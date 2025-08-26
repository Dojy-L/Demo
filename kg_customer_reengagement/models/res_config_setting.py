# -*- coding: utf-8 -*-
from ast import literal_eval
from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"



    inactive_days = fields.Integer(
        string="Inactive Days",
        # domain="[('usage', '=', 'internal')]"
        config_parameter='kg_material_request.inactive_days'
    )

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()

        inactive_days_str = params.get_param('kg_customer_reengagement.inactive_days')



        res.update(inactive_days=int(inactive_days_str) if inactive_days_str else False)

        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        inactive_days_id = self.inactive_days if self.inactive_days else False


        self.env['ir.config_parameter'].sudo().set_param(
            'kg_customer_reengagement.inactive_days', inactive_days_id
        )
