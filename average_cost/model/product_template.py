# -*- coding: utf-8 -*-

from odoo import fields,models

class ProductTemplate(models.Model):
    """Add a field in product.product"""
    _inherit = 'product.product'

    average_cost = fields.Float(String='Average Cost', compute="_compute_average_cost")

    def _compute_average_cost(self):
        """calculate the average cost"""
        for rec in self:
            quantity = rec.purchased_product_qty
            if quantity:
                total =  rec.purchase_order_line_ids.filtered(lambda n: n.state == 'purchase').mapped('price_subtotal')
                average = sum(total)/quantity

                if average:
                    rec.average_cost = average
                else:
                    rec.average_cost = 0
            else:
                rec.average_cost = 0

