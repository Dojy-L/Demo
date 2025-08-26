# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Portal Documents',
    'version': '17.0.1.0.0',
    'category': '',
    'summary': '',
    'description': """Portal Documents""",
    'depends': ['base', 'sale', 'stock','documents','website' ],
    'data': [
    #     'security/ir.model.access.csv',
    #     'security/material_groups.xml',
    #
    #     'data/mtr_sequence.xml',
    #     'views/material_request.xml',
        'views/document_template.xml'
    #
    #     'wizard/reject_reason_wizard.xml',
    #
    ],

    'sequence': -1,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
