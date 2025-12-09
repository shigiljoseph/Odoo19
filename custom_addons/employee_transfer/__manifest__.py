# -*- coding: utf-8 -*-
{
    'name' : 'User Transfers Request',
    'version':'19.0.1.0.0',
    'sequence':1,
    'data':[
        'security/ir.model.access.csv',
        'views/transfer_request_view.xml',
        'views/employee_transfer_menu.xml',
    ],
    'depends':['base','hr','mail'],
    'license': 'LGPL-3',
    "application": True,
    'author': 'Odoo S.A.',
    'summary':'user can create transfer request from one company to another company.'
}

