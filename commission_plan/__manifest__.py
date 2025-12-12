# -*- coding: utf-8 -*-

{
    "name": 'Commission Plan',
    'version':'19.0.1.0.0',
    'sequence':1,
    'data':[
        'security/ir.model.access.csv',
        'views/crm_commission_views.xml',
        'views/crm_team_views.xml',
        'views/crm_team_member_views.xml',
        'views/sale_order_views.xml',
        'views/commission_history_views.xml',
        'views/res_users_views.xml',
        'views/crm_commission_menu_views.xml',
    ],
    'depends':['base','crm','sale','mail'],
    'license': 'LGPL-3',
    "application": True,
    'author': 'Odoo S.A.',
    'summary':'To create commision plan for sales person'
}