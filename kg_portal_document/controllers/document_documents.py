from odoo import http, fields
from odoo.http import request
from datetime import datetime, timedelta, timezone, date
from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from datetime import datetime
import pytz

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class DocumentPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        vcc = super()._prepare_home_portal_values(counters)
        # print(vcc, 'ffffffffffffffff')
        vcc['att_count'] = request.env['document.documents'].search_count([])
        return vcc

    @http.route(['/my/documents'], type='http', auth="user", website=True)
    def portal_attendance_page(self, **kw):
        user = request.env.user
        return request.render('kg_material_request.attendance_template', {
            'user': user
        })

