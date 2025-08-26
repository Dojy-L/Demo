from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection(selection_add=[
        ('requested', 'Requested'), ('approve','approve')
    ])



    def kg_request_approve(self):
        print("kg_request_approve")

    def action_stock_approve(self):
        print("action_stock_approve")


