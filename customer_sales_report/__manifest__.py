# -*- coding: utf-8 -*-

{
    'name' : 'Customer Sale Report',
    'version': '19.0.1.0.0',
    'sequence':2,
    "data":[
        'security/ir.model.access.csv',
        'data/ir.cron.xml',
        'report/customer_sale_report_template.xml',
        'report/customer_sale_report.xml',
        'data/customer_sale_report_email_template.xml',
        'views/customer_sale_report_views.xml',
    ],
    'depends':['base','sale'],
    "application": True,
    'license': 'LGPL-3',
    'author': 'Odoo S.A.',
    'auto_install': False,
    'summary':'To generate and send send sales report to selected customers.'
}

