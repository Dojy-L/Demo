# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Demo Purchase',
    'version': '17.0.1.0.0',
    'category': '',
    'summary': '',
    'description': """Purchase""",
    'depends': ['base', 'purchase', 'product','sale','stock'],
    'data': [
        'views/account_move.xml',


    ],

    'sequence': -1,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}