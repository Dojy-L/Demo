# -*- coding: utf-8 -*-
from ast import literal_eval
from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"



    destination_id = fields.Many2one(
        'stock.location',
        string="Destination Location",
        # domain="[('usage', '=', 'internal')]"
        config_parameter='kg_material_request.destination_id'
    )

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()

        destination_id_str = params.get_param('kg_material_request.destination_id')



        res.update(destination_id=int(destination_id_str) if destination_id_str else False)

        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        destination_id = self.destination_id.id if self.destination_id else False


        self.env['ir.config_parameter'].sudo().set_param(
            'kg_material_request.destination_id', destination_id
        )
