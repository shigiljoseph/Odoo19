# -*- coding: utf-8 -*-

{
    'name' : 'Sale Order Migration',
    'version': '19.0.1.0.0',
    'sequence':2,
    "data":[
        'security/ir.model.access.csv',
        'wizard/migration_wizard.xml',
        'views/sale_order_migrate_menu_view.xml',

    ],
    'depends':['base','sale'],
    "application": True,
    'license': 'LGPL-3',
    'author': 'Odoo S.A.',
    'auto_install': False,
    'summary':'To migrate sale order from odoo 18 to 19.'
}

