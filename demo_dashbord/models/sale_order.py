from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def get_sale_order_data(self):
        print("get_sale_order_data")
        sale_data = []
        sale_order_data = self.env['sale.order'].search([()])
        for sale in sale_order_data:
            # state = dict(line._fields['status'].selection).get(line.status, '') if line else ''
            # utilization = dict(line._fields['utilization'].selection).get(line.utilization, '') if line else ''
            sale_data.append({
                'id' : sale.id,
                'name' : sale.name,

            })
        return {'vals': sale_data,}


