# -*- coding: utf-8 -*-

{
    'name' : 'Product Average Cost',
    'version':'19.0.1.0.0',
    'sequence':1,
    'data':[
        'views/product_template_view.xml',
    ],
    'depends':['base','purchase','mail'],
    'license': 'LGPL-3',
    "application": True,
    'author': 'Odoo S.A.',
    'summary':'Find the average cost from all the previous purchase of the product.'
}