# -*- coding: utf-8 -*-

{
    'name' : 'New Module',
    'version': '19.0.1.0.0',
    'sequence':2,
    'depends': ['website', 'base', 'web'],
    "data":[
        'views/templates.xml',
        'views/shop_template.xml',
        'views/todo_template.xml',

    ],
    'assets':{
    'web.assets_frontend': [
        'new_module/static/src/js/example.js',
        'new_module/static/src/js/event_interaction.js',
        ]
    },
    "application": True,
    'license': 'LGPL-3',
    'author': 'Odoo S.A.',
    'auto_install': False,
    'summary':'New Module'
}