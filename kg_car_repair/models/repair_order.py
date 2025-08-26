from odoo import models, fields, _, api
from odoo.exceptions import ValidationError, AccessError


class RepairOrder(models.Model):
    _inherit = "repair.order"
    _description = "Repair Order"


    vehicle_no = fields.Char(string="Vehicle Number", required=True)


    # name = fields.Char(string="Reference", required=True,
    #                    readonly=True, default=lambda self: _('New'))
    # partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    # email = fields.Char(string="Email", related='partner_id.email')
    # phone = fields.Char(string="Phone", related='partner_id.phone')
    # service_type_id = fields.Many2one('service.type', string="Service Type")
    # booking_date = fields.Datetime(string="Booking Date", default=lambda self: fields.Datetime.now())
#     car_mileage = fields.Float(string="Mileage(km)")
#     brand = fields.Many2one('car.brand', string="Brand")
#     repair_reason = fields.Text(string="Repair Reason", required=True)
#     car_model = fields.Char(string="Car Model")
#     car_color = fields.Char(string="Car Color")
#     state = fields.Selection(
#         [('draft', 'Draft'),
#          ('submitted', 'Submitted'),
#          ('approve', 'Approved'),
#          ('in_progress', 'In Progress'),
#          ('repaired', 'Repaired'),
#          ('done', 'Done'),
#          ('reject', 'Reject'),
#          ('cancel', 'Cancel')],
#         string='Status', default='draft', readonly=True, tracking=True)
#     notes = fields.Html('Notes')
#
#     @api.model
#     def _get_technician_domain(self):
#         group = self.env.ref('kg_car_repair.car_repair_request_user_technician', raise_if_not_found=False)
#         if group:
#             return [('groups_id', 'in', [group.id])]
#         return []
#
#     technician_id = fields.Many2one(
#         'res.users',
#         string='Assigned Technician',
#         domain=lambda self: self._get_technician_domain()
#     )
#     car_image = fields.Binary(String="Car Image")
#     estimation_line_ids = fields.One2many('car.repair.estimation.line', 'repair_id', string='Estimation Lines')
#     car_inv_ids = fields.Many2many('account.move', string="Car Invoice", relation='move_rel')
#     move_count = fields.Integer(string="Transfer Count" ,compute='_compute_move_count')
#
#
#     @api.model_create_multi
#     def create(self, vals_list):
#         for vals in vals_list:
#             vals['name'] = self.env['ir.sequence'].next_by_code('car.repair.sequence') or 'New'
#         return super(CarRepair, self).create(vals_list)
#
#     def action_submit_button(self):
#         self.state = 'submitted'
#
#     def action_reject_button(self):
#         self.state = 'reject'
#
#     def action_cancel_button(self):
#         self.state = 'cancel'
#
#     def action_reset_to_draft_button(self):
#         self.state = 'draft'
#
#     def button_approve(self):
#         print("button_approve")
#         for record in self:
#             if not record.technician_id:
#                 raise ValidationError(_('Please select a Technician before approving the request.'))
#             if not self.env.user.has_group('kg_car_repair.car_repair_request_group_admin'):
#                 raise AccessError(_('You do not have access to approve this request.'))
#             record.state = 'approve'
#             record.message_post(
#                 body=_("The request has been approved by %s.") % self.env.user.name
#             )
#             # Send email to technician
#             if record.technician_id.partner_id.email:
#                 mail_values = {
#                     'subject': _('New Repair Request Assigned: %s') % record.name,
#                     'body_html': _(
#                         "<p>Hello %s,</p>"
#                         "<p>You have been assigned a new car repair request: <strong>%s</strong>.</p>"
#                         "<p>Please check the details in the system.</p>"
#                     ) % (record.technician_id.name, record.name),
#                     'email_to': record.technician_id.email,
#                     'auto_delete': True,
#                     'model': 'car.repair',
#                     'res_id': record.id,
#                 }
#                 self.env['mail.mail'].create(mail_values).send()
#
#     def button_start_repair(self):
#         print("button_start_repair")
#         self.state = 'in_progress'
#
#     def action_repaired(self):
#         print("action_repaired")
#         self.state = 'repaired'
#
#     def action_create_invoice(self):
#         self.ensure_one()
#         if not self.estimation_line_ids:
#             raise ValidationError(_('You cannot create an invoice without repair estimation lines.'))
#         car_moves = self.env['account.move'].create({
#             'move_type': 'out_invoice',
#             'partner_id': self.partner_id.id,
#             'invoice_date': self.booking_date or fields.Date.today(),
#             'invoice_origin': self.name,
#             # 'id': self.id,
#         })
#
#         moves = [(0, 0, {
#             'product_id': line.product_id.id,
#             'quantity': line.quantity,
#             'price_unit': line.price_unit,
#             # 'tax_ids': [(6, 0, line.product_id.taxes_id.ids)],
#         }) for line in self.estimation_line_ids]
#
#         car_moves.write({'invoice_line_ids': moves})
#         car_moves.action_post()
#         self.car_inv_ids = [(4, car_moves.id)]
#         # self.car_inv_ids = [(6, 0, car_moves.ids)]
#         # self.state = 'payed'
#         # return {
#         #     'type': 'ir.actions.act_window',
#         #     'res_model': 'account.move',
#         #     'res_id': car_moves.id,
#         #     'view_mode': 'form',
#         #     'target': 'current',
#         # }
#
#     def action_get_invoice_record(self):
#         print("action_get_invoice_record")
#         self.ensure_one()
#         return {
#             'name': _('Customer Invoices'),
#             'type': 'ir.actions.act_window',
#             'res_model': 'account.move',
#             'view_mode': 'list,form',
#             'domain': [('invoice_origin', '=', self.name), ('move_type', '=', 'out_invoice')],
#             'context': {'default_partner_id': self.partner_id.id},
#         }
#
#     @api.depends('car_inv_ids')
#     def _compute_move_count(self):
#         print("_compute_move_count")
#         for rec in self:
#             if rec.car_inv_ids:
#                 rec.move_count = len(rec.car_inv_ids)
#             else:
#                 rec.move_count = 0
#
#
#
#
# class CarRepairEstimationLine(models.Model):
#     _name = 'car.repair.estimation.line'
#     _description = 'Car Repair Estimation Line'
#
#     repair_id = fields.Many2one('car.repair', string='Repair Reference')
#     product_id = fields.Many2one('product.product', string='Product', required=True)
#     quantity = fields.Float(string='Quantity', required=True)
#     price_unit = fields.Float(string='Unit Price', required=True)
#     uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
#
#     @api.onchange('product_id')
#     def _onchange_product_id(self):
#         for line in self:
#             if line.product_id:
#                 line.uom_id = line.product_id.uom_id.id
#                 line.price_unit = line.product_id.lst_price
