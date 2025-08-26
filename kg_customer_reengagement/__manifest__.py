# -*- coding: utf-8 -*-

# Klystron Global LLC
# Copyright (C) Klystron Global LLC
# All Rights Reserved
# https://www.klystronglobal.com/

{
    'name': 'Customer Re-Engagement',
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['base','sale','purchase', 'mail','sale_management','website_sale'],
    'sequence': '-100',
    'author': 'Klystron Global',
    'maintainer': 'Dojy Larsan',
    'website': "www.klystronglobal.com",
    'application': True,
    'description': """The module is used to detect inactive customers (e.g., no purchases in the last X days) and trigger a personalized re-engagement email with a discount.""",
    'data': [
        'security/ir.model.access.csv',
        'data/rerengament_cron.xml',
        'data/email_template.xml',
        'views/res_config_setting.xml',
    ],
    'installable': True,
    'demo': [],

}