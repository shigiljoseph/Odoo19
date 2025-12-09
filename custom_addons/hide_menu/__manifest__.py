# -*- coding: utf-8 -*-

{
    'name' : 'Hide menu for User',
    'version': '19.0.1.0.0',
    'sequence':2,
    "data":[
        # 'security/record_rules.xml',
        'views/res_users_view.xml',
    ],
    'depends':['base'],
    "application": True,
    'license': 'LGPL-3',
    'author': 'Odoo S.A.',
    'auto_install': False,
    'summary':'Allow configuration to hide specific menus for users.'
}

