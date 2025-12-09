# -*- coding: utf-8 -*-

from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleInherit(WebsiteSale):

    def shop(self,page=0,category=None,search='',**post):
        response = super().shop(page=0,category=None,search='',**post)
        response.qcontext['custom_data'] = 'My custom Value'

        print(response)
        return response
