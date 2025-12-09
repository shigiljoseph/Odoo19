# -*- coding: utf-8 -*-

{
    "name":"Aproval block",
    'version': '19.0.1.0.0',
    'sequence':2,
    "data":[
        'security/ir.model.access.csv',
        'data/approval_block_data.xml',
        'views/purchase_order_views.xml',
    ],
    'depends':['base','purchase'],
    "application": True,
    'license': 'LGPL-3',
    'author': 'Odoo S.A.',
    'auto_install': False,
    'summary':'To add approval block on purchase order'

}