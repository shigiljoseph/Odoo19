# -*- coding: utf-8 -*-
{
    'name' : 'POS Discount Limit',
    'version' : '19.0.1.0.0',
    'sequence' : 2,
    "data" : [
        'views/pos_settings_view.xml',
    ],
    'depends' : ['base','pos_sale'],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_discount_limit/static/src/js/**/*',
            'pos_discount_limit/static/src/xml/**/*',
        ],
    },
    "application" : True,
    'license' : 'LGPL-3',
    'author' : 'Odoo S.A.',
    'auto_install' : False,
    'summary' : 'To limit the discount based on the product category'
}