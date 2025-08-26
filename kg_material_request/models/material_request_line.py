# -*- coding: utf-8 -*-

from odoo import fields, models, _, api


class MaterialRequestLine(models.Model):
    _name = "material.request.line"
    _description = "Material Request Line"

    product_id = fields.Many2one('product.product',string="Product", required=True,domain=[('detailed_type', '=', 'product')])
    description = fields.Char(string="Description",related='product_id.name')
    quantity = fields.Float(string="Quantity", required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', related='product_id.uom_id')
    unit_price = fields.Float(string="Unit Price",related='product_id.lst_price')
    subtotal = fields.Float(string="Subtotal", compute='_compute_subtotal')
    customer_id = fields.Many2one("res.partner", string="Customer", required=True)

    material_id = fields.Many2one('kg.material.request', string="Material id")

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price

    class SaleOrderInherit(models.Model):
        _inherit = "sale.order"

        request_id = fields.Many2one('kg.material.request')


    class StockPicking(models.Model):
        _inherit = "stock.picking"

        request_id = fields.Many2one('kg.material.request')

