# -*- coding: utf-8 -*-
from collections import defaultdict

from odoo import fields, models, _, api
from odoo.exceptions import UserError
from ast import literal_eval


class KgMaterialRequest(models.Model):
    _name = "kg.material.request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Kg Material Request"
    _order = 'name desc'

    name = fields.Char(string='Reference', required=True,
                       readonly=True, default=lambda self: _('New'))

    employee_id = fields.Many2one('hr.employee','Employee',required=True)
    request_date = fields.Date(string="Request Date", default=lambda self: fields.Date.context_today(self))
    requested_by = fields.Many2one('res.partner',string="Requested By")
    requested_by_id = fields.Many2one('res.users',string="Requested By",default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company',string="Company",default=lambda self: self.env.company)
    type = fields.Selection([('sale', 'Create Sale Order'), ('internal', "Create Transfer")], string='Request Type',default='sale')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('request', 'Requested'),
            ('approve', 'Approved'),
            ('reject', 'Rejected'),
            ('sale', 'Sale Order'),
            ('internal', 'Transfer'),
            ('cancel', 'Cancelled'),
        ],
        string='States',
        tracking=True,
        default='draft',
    )

    approved_by = fields.Many2one('res.users',string="Approved By", readonly=True)
    approve_date = fields.Date(string="Approved Date", readonly=True)
    notes = fields.Html('Notes')

    rejected_by = fields.Many2one('res.users',string="Rejected By", readonly=True)
    reject_date = fields.Date(string="Reject Date", readonly=True)
    reject_reason = fields.Text(string="Reject Reason", readonly=True)

    material_line_ids =  fields.One2many('material.request.line','material_id',string="material line ids")
    is_request_for_approval = fields.Boolean(default=True)
    source_location_id = fields.Many2one('stock.location', domain="[('usage', '=', 'internal')]")

    internal_transfer_ids = fields.One2many(
        'stock.picking', 'origin', string='Internal Transfers', relation='internal_stock_rel',
        domain=[('picking_type_id.code', '=', 'internal')]
    )
    sale_order_ids = fields.Many2many('sale.order', string="Sale Orders")
    stock_ids = fields.Many2many('stock.picking', string="Transfer", relation='stock_rel')

    transfer_count = fields.Integer(string="Transfer Count" ,compute='_compute_transfer_count')
    sale_count = fields.Integer(string="Transfer Count" , compute='_compute_sale_count')

    def _compute_sale_count(self):
        for rec in self:
            if rec.sale_order_ids:
                rec.sale_count = len(rec.sale_order_ids)
            else:
                self.sale_count = 0

    def _compute_transfer_count(self):
        for rec in self:
            if rec.stock_ids:
                rec.transfer_count = len(rec.stock_ids)
            else:
                self.transfer_count = 0


    def action_request_for_approval_button(self):
        for rec in self:
            if not rec.material_line_ids:
                raise UserError(_("Please select the products."))

            rec.state='request'
            rec.send_mail()

    def action_cancel_button(self):
        self.state = 'cancel'

    def action_reset_to_draft_button(self):
        for rec in self:
            if rec.type == 'sale':
                confirmed_sale_orders = rec.sale_order_ids.filtered(lambda so: so.state != 'draft')
                if confirmed_sale_orders:
                    raise UserError(_("Cannot reset to draft. The associated sale orders are confirmed."))
                rec.state = 'draft'
            if rec.type == 'internal':
                stock_orders = rec.stock_ids.filtered(lambda so: so.state != 'draft')
                if stock_orders:
                    raise UserError(_("Cannot reset to draft. The associated sale orders are confirmed."))
                rec.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('kg.material.request.sequence') or '/'
        return super(KgMaterialRequest, self).create(vals_list)


    def action_approve_button(self):
        for rec in self:
            rec.state = 'approve'
            rec.approved_by = self.env.user.id
            rec.approve_date = fields.Date.today()
            rec.send_approval_notification()

    def action_reject_button(self):
        return {
            'name': _('Reject Reason'),
            'type': 'ir.actions.act_window',
            'res_model': 'rejects.reason.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_material_id': self.id,  # Pass the material request ID to the wizard
            }
        }

        self.state = 'reject'



    def action_create_sale_order_button(self):
        """ Create Sale Orders for each unique Customer in the Material Request """
        if not self.material_line_ids:
            raise UserError(_('No materials found to create a Sale Order.'))

        customer_lines_map = {}
        for line in self.material_line_ids:
            if not line.customer_id:
                raise UserError(_('All products must have a customer assigned.'))

            if line.customer_id.id not in customer_lines_map:
                customer_lines_map[line.customer_id.id] = []
            customer_lines_map[line.customer_id.id].append(line)

        sale_orders = []

        for customer_id, lines in customer_lines_map.items():
            sale_order = self.env['sale.order'].create({
                'partner_id': customer_id,
                'date_order': fields.Datetime.now(),
                'company_id': self.company_id.id,
                'request_id':self.id,
                'order_line': [(0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.description,
                    'product_uom_qty': line.quantity,
                    'price_unit': line.unit_price,
                    'product_uom': line.uom_id.id
                }) for line in lines]
            })
            sale_orders.append(sale_order.id)
        self.sale_order_ids = [(6, 0, sale_orders)]
        self.state = 'sale'


    def action_internal_transfer_button(self):
        stock_location_from = self.source_location_id
        stock_location_to_str = self.env['ir.config_parameter'].sudo().get_param('kg_material_request.destination_id')
        stock_location_to = literal_eval(stock_location_to_str) if stock_location_to_str else None
        operation_from_type_id = self.env['stock.picking.type'].sudo().search([
            ('code', '=', 'internal'),
            ('company_id', '=', self.company_id.id)
        ], limit=1)

        if not stock_location_to:
            raise UserError('Please configure Internal location')

        customer_material_lines = defaultdict(list)
        for line in self.material_line_ids:
            customer_material_lines[line.customer_id].append(line)

        stock_picking_env = self.env['stock.picking']

        created_pickings = []

        for customer, lines in customer_material_lines.items():
            picking = stock_picking_env.create({
                'partner_id': customer.id,
                'picking_type_id': operation_from_type_id.id,
                'location_id': stock_location_from.id,
                'location_dest_id': int(stock_location_to),
                'date': self.request_date or fields.Date.today(),
                'origin': self.name,
                'request_id': self.id,
            })

            created_pickings.append(picking.id)

            moves = [(0, 0, {
                'partner_id': customer.id,
                'picking_id': picking.id,
                'product_uom_qty': line.quantity,
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_uom': line.uom_id.id,
                'location_id': stock_location_from.id,
                'location_dest_id': int(stock_location_to),
            }) for line in lines]


            picking.write({'move_ids': moves})
        self.stock_ids = [(6, 0, created_pickings)]
        self.state = 'internal'

        print(f"Created Stock Pickings: {created_pickings}")

    def action_view_transfer(self):
        print("action_view_transfer")
        self.ensure_one()
        return {
            'name': 'Transfer',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': [('request_id','=',self.id)],
        }

    def action_view_quotations(self):
        self.ensure_one()
        return {
            'name': 'Sale Order',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.sale_order_ids.ids)],
        }

    def send_mail(self):
        """Send email notification to approvers when a material request is submitted for approval"""
        approval_group = self.env.ref('kg_material_request.material_request_group_approval')
        approval_users = approval_group.users.filtered(lambda u: u.email)

        if not approval_users:
            raise UserError(_("No approvers found with email addresses!"))

        recipient_emails = [user.email for user in approval_users]

        subject = _("Material Request Approval Required")
        body = _(
            """
            <p>Dear Approver,</p>
            <p>A new Material Request has been submitted by <strong>%s</strong> and requires your approval.</p>
            <p><strong>Reference:</strong> %s</p>
            <p><strong>Requested Date:</strong> %s</p>
            <p><strong>Requested By:</strong> %s</p>
            <p>Please review the request and take necessary action.</p>
            <p><a href="%s">Click here to view the request</a></p>
            <p>Thank you.</p>
            """
        ) % (
                   self.requested_by_id.name,
                   self.name,
                   self.request_date,
                   self.requested_by_id.name,
                   self.get_material_request_url(),
               )

        outgoing_mail_server = self.env['ir.mail_server'].sudo().search([], limit=1)
        email_from = outgoing_mail_server.sudo().smtp_user if outgoing_mail_server else self.env.user.email

        mail_values = {
            'subject': subject,
            'body_html': body,
            'email_to': ', '.join(recipient_emails),
            'email_from': email_from,
        }

        self.env['mail.mail'].sudo().create(mail_values).send()

    def get_material_request_url(self):
        """Generate the URL for approvers to view the material request"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/web#id={self.id}&view_type=form&model={self._name}"

    def send_approval_notification(self):
        """Send email notification to the requester upon approval"""
        if not self.requested_by_id.email:
            raise UserError(_("The requester does not have an email address!"))

        subject = _("Your Material Request Has Been Approved")
        body = _(
            """
            <p>Dear %s,</p>
            <p>Your material request <strong>%s</strong> has been approved by <strong>%s</strong>.</p>
            <p><strong>Approved Date:</strong> %s</p>
            <p>You can view the approved request here:</p>
            <p><a href="%s">Click here to view</a></p>
            <p>Thank you.</p>
            """
        ) % (
                   self.requested_by_id.name,
                   self.name,
                   self.approved_by.name,
                   self.approve_date,
                   self.get_material_request_url(),
               )

        outgoing_mail_server = self.env['ir.mail_server'].sudo().search([], limit=1)
        email_from = outgoing_mail_server.sudo().smtp_user if outgoing_mail_server else self.env.user.email

        mail_values = {
            'subject': subject,
            'body_html': body,
            'email_to': self.requested_by_id.email,
            'email_from': email_from,
        }

        self.env['mail.mail'].sudo().create(mail_values).send()

