from odoo import models, fields,api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_car = fields.Boolean(string="Is Car", default=False)

    @api.model_create_multi
    def create(self, vals):
        result = super(ProductTemplate, self).create(vals)
        self.is_car = True

        return result