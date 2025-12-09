# -*- coding: utf-8 -*-

{
    'name' : 'sale Order Payment',
    'version': '19.0.1.0.0',
    'sequence':2,
    "data":[
        'views/sale_order_view.xml'
    ],
    'depends':['base','sale'],
    "application": True,
    'license': 'LGPL-3',
    'author': 'Odoo S.A.',
    'auto_install': False,
    'summary':'Option to directly register payment from sale order.'
}