# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Appointment Booking',
    'version': '17.0.1.0.0',
    'category': '',
    'summary': '',
    'description': """Appintment Booking""",
    'depends': ['base', 'appointment', 'product','sale'],
    'data': [
        'security/ir.model.access.csv',
        # 'security/material_groups.xml',

        # 'data/mtr_sequence.xml',
        # 'views/material_request.xml',
        'views/appointment_booking.xml',
        #
        # 'wizard/reject_reason_wizard.xml',

    ],

    'sequence': -1,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}