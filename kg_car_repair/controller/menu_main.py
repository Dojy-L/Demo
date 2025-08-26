from datetime import datetime

from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo import http
from odoo.http import request


class PortalCarRepair(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        cvv = super()._prepare_home_portal_values(counters)
        cvv['repair_count'] = request.env['car.repair'].search_count([])
        return cvv

    @http.route('/car_repair_form', type='http', auth='user', website=True)
    def repair_request_form(self, **kwargs):
        customer_data = request.env['repair.order'].sudo().search([])
        product_data = request.env['product.product'].sudo().search([])
        tag_data = request.env['repair.tags'].sudo().search([])
        # repair_data = request.env['car.repair'].sudo().search([z])
        # type_data = request.env['service.type'].sudo().search([])
        # brand_data = request.env['car.brand'].sudo().search([])
        # print(repair_data, "repair_datarepair_data")

        user = request.env.user
        print("useruser",user.name)
        values = {
            'partner_id': user.name if user else '',
            'customer_data': customer_data,
            'product_data': product_data,
            'tag_data': tag_data,
            # 'repair_data': repair_data,
            # 'types': type_data,
            # 'brands': brand_data,

        }
        print("valuesvalues",values)
        return request.render('kg_car_repair.portal_car_repair_request_form', values)

    @http.route('/car_repair_form/submit', type='http', auth='user', website=True, csrf=True)
    def submit_repair_request(self, **post):
        # Convert booking_date to datetime format
        booking_date = post.get('booking_date')
        if booking_date:
            booking_date = datetime.strptime(booking_date, '%Y-%m-%dT%H:%M')
        else:
            booking_date = False

        # Prepare values for car.repair creation
        repair_values = {
            'partner_id': request.env.user.partner_id.id,
            'product_id': int(post.get('product_id')) if post.get('product_id') else False,
            # 'vehicle_no': post.get('vehicle_no'),
            # 'car_mileage': float(post.get('mileage')) if post.get('mileage') else 0.0,
            # 'mileage': post.get('mileage'),
            # 'brand': int(post.get('brand_id')) if post.get('brand_id') else False,
            'tag_ids': int(post.get('repair_tag_id')) if post.get('repair_tag_id') else False,
            # 'car_model': post.get('car_model'),
            # 'car_color': post.get('car_color'),
            'internal_notes': post.get('repair_reason'),
            # 'booking_date': booking_date,
            'schedule_date': booking_date,
            'state': 'draft',  # Set initial state
        }
        print("repair_valuesrepair_values",repair_values)

        # Create the repair record
        request.env['repair.order'].sudo().create(repair_values)
        # return request.redirect('/my')
        return request.redirect('repair/thank_you')

    @http.route('/repair/thank_you', type='http', auth='user', website=True)
    def thank_you_time_off(self, **kwargs):
        return request.render('kg_car_repair.car_repair_request_thanks')