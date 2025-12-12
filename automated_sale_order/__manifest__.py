# -*- coding: utf-8 -*-

{
    'name':"Automated Sale Order",
    'version': '1.3',
    'sequence':1,
    'depends' : ['base','sale'],
    'data':[
        'security/ir.model.access.csv',
        'wizard/buy_product_views.xml',
        'views/product_template.xml',
    ],
    "application": True,
    'license': 'LGPL-3'
}