# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from markupsafe import Markup


class CustomShop(http.Controller):

    @http.route('/shop/custom',type='http',auth='public',website=True)
    def custom_shop(self,**Kwargs):
        products = request.env['product.product'].sudo().search([],limit=12)

        print('env',request.env)
        print('params',request.params)
        print('httprequest',request.httprequest)
        print('website',request.website)
        print('session',request.session)
        print('cr',request.cr)
        print('uid',request.uid)

        return request.render('new_module.custom_shop',{
            'products': products,
            'page_title' : 'Custom Shop',
            'markup':'<span>Hai welcome</span> '
        })