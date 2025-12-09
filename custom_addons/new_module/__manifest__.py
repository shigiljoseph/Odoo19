# -*- coding: utf-8 -*-

{
    'name' : 'New Module',
    'version': '19.0.1.0.0',
    'sequence':2,
    "data":[
        'views/templates.xml',
        'views/shop_template.xml'
    ],
    'assets':{
    'web.assets_frontend': [
        'new_module/static/src/js/example.js',
        ]
    },
    'depends':['base','website'],
    "application": True,
    'license': 'LGPL-3',
    'author': 'Odoo S.A.',
    'auto_install': False,
    'summary':'New Module'
}