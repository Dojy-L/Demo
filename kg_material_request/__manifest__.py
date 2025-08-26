# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Material Request',
    'version': '17.0.1.0.0',
    'category': '',
    'summary': '',
    'description': """Material Request""",
    'depends': ['base', 'sale', 'stock', ],
    'data': [
        'security/ir.model.access.csv',
        'security/material_groups.xml',

        'data/mtr_sequence.xml',
        'views/material_request.xml',
        'views/res_settings.xml',

        'wizard/reject_reason_wizard.xml',

    ],

    'sequence': -1,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
