# -*- coding: utf-8 -*-

# Klystron Global LLC
# Copyright (C) Klystron Global LLC
# All Rights Reserved
# https://www.klystronglobal.com/

{
    'name': 'Car repair Management',
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['base','sale','website', 'contacts', 'portal','product','mail','repair'],
    'sequence': '-100',
    'author': 'Klystron Global',
    'maintainer': 'Dojy Larsan',
    'website': "www.klystronglobal.com",
    'application': True,
    'description': """The module is used for Car Repair Management in odoo""",
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/car_repair_groups.xml',

        # 'data/car_repair_sequence.xml',
        'data/website_menu.xml',

        'views/repair_request_form_template.xml',
        # 'views/car_product_views.xml',
    ],

    'installable': True,
    'demo': [],

}