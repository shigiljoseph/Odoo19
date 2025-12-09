# -*- coding: utf-8 -*-

from odoo import api,fields,models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    product_ids = fields.Many2many(
        'product.product',compute='_compute_products',
        string='Partner Products',store=True )


    @api.depends('partner_id')
    def _compute_products(self):
        """select the product_ids of partner"""
        print('hii')
        domain = []
        if self.partner_id.product_ids:
            domain = [('id', '=', self.partner_id.product_ids)]
            print(domain)
            self.order_line.update({
                'product_id': [
                    (fields.Command.set(self.product_ids.search(domain).ids))]
            })
        self.update({
            'product_ids': [
                (fields.Command.set(self.product_ids.search(domain).ids))]
        })
        print(self.product_ids)


