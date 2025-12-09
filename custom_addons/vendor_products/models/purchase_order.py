# -*- coding: utf-8 -*-

from odoo import api,fields,models


class PurchaseOrder(models.Model):
    """Add field and  set product domain"""
    _inherit = 'purchase.order'

    is_vendor_products = fields.Boolean(string='Vendor Products')
    product_ids = fields.Many2many('product.product')

    @api.onchange('is_vendor_products', 'partner_id')
    def _onchange_vendor_products(self):
        """select the product_ids of vendor"""
        domain = []
        if self.is_vendor_products:
            domain = [('seller_ids.partner_id', '=', self.partner_id)]
            print(domain)
        self.update({
            'product_ids': [
                (fields.Command.set(self.product_ids.search(domain).ids))]
        })
