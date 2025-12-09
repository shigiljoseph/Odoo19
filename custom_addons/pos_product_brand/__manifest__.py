# -*- coding: utf-8 -*-

{
    'name' : 'POS Product Brand',
    'version': '19.0.1.0.0',
    'sequence':2,
    "data":[
        'security/ir.model.access.csv',
        'views/product_template_view.xml',
        'views/product_brand_view.xml',

    ],
    'depends':['base','pos_sale'],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_product_brand/static/src/xml/pos_orderline.xml',
        ],
    },
    "application": True,
    'license': 'LGPL-3',
    'author': 'Odoo S.A.',
    'auto_install': False,
    'summary':'To show the bill of materials of the products'
}