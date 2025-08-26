from odoo import http, fields
from odoo.http import request, _logger
from datetime import datetime, timedelta, timezone, date
from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from datetime import datetime
import pytz
import base64
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class CarRepairPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        vcc = super()._prepare_home_portal_values(counters)
        vcc['request_count'] = request.env['car.repair'].search_count([])
        print(vcc, 'cccccccccccccccc')
        return vcc

    @http.route('/my/request', type='http', website=True, auth="user")
    def PortalEmployeeDocuments(self, **kw):
        repair = request.env['car.repair'].sudo().search([])
        repair_list = []
        for rec in repair:
            # typ = dict(rec._fields['type'].selection).get(rec.type, '') if rec else ''
            repair_list.append({
                'record': rec,
                'partner': rec.partner_id.name,
                'booking_date': rec.booking_date,
                'type': rec.service_type_id.name,
                # 'type': typ,
                'name': rec.name,
                'number': rec.vehicle_no,

            })
        vals = {'repair': repair_list}
        return request.render('kg_car_repair.portal_car_repair_list_view',vals)
