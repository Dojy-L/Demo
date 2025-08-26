# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Demo Dashboard',
    'version': '17.0.1.0.0',
    'category': '',
    'summary': '',
    'description': """Demo Dashboard""",
    'depends': ['base', 'product','sale','sale_management'],
    'data': [
        'views/sale_dashboard_menu.xml'

    ],
    "assets": {
        "web.assets_backend": [
            'demo_dashbord/static/src/js/sale_dashboard.js',
            'demo_dashbord/static/src/xml/sale_dashboard_template.xml',
            ]
    },

    'sequence': -1,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}