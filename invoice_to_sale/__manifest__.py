# -*- coding: utf-8 -*-

{
    'name' : 'Invoice to  Sale',
    'version': '19.0.1.0.0',
    'sequence':2,
    "data":[
        'views/account_move_form_views.xml',
    ],
    'depends':['base','sale'],
    "application": True,
    'license': 'LGPL-3',
    'author': 'Odoo S.A.',
    'auto_install': False,
    'summary':'Option to directly create and link sale order from invoice.'
}