# -*- coding: utf-8 -*-

{
    'name' : 'Website BOM',
    'version': '19.0.1.0.0',
    'sequence':2,
    "data":[
        'views/website_settings_view.xml',
        'views/website_cart.xml'
    ],
    'depends':['base','website','website_sale','sale'],
    "application": True,
    'license': 'LGPL-3',
    'author': 'Odoo S.A.',
    'auto_install': False,
    'summary':'To show the bill of materials of the products'
}