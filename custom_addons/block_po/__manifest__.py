# -*- coding: utf-8 -*-

{
    'name' : 'Block PO',
    'version': '19.0.1.0.0',
    'sequence':2,
    "data":[
        'security/ir.model.access.csv',
        'wizard/create_order_views.xml',
        # 'data/action_list.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/sale_order_line_view.xml',
        'views/sale_order_menu.xml',


    ],
    'depends':['base','purchase','sale'],
    "application": True,
    'license': 'LGPL-3',
    'author': 'Odoo S.A.',
    'auto_install': False,
    'summary':'Block vendor and give warning if overdue'
}

