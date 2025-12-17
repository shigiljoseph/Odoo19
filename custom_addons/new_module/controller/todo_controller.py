# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from markupsafe import Markup


class CustomShop(http.Controller):

    @http.route('/custom/todo',type='http',auth='public',website=True)
    def custom_shop(self,**Kwargs):
        return request.render('new_module.custom_todo',{
            'page_title' : 'Custom To Do',
            'markup':'<span>Hai welcome</span> '
        })