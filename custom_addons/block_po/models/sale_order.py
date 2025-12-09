# -*- coding: utf-8 -*-

from odoo import fields,models
from odoo.exceptions import UserError


class saleOrder(models.Model):
    """Add fields and check order line"""
    _inherit = 'sale.order'

    premium = fields.Boolean(related='partner_id.premium')
    value = fields.Integer(related='partner_id.value')

    def action_confirm(self):
        """To check the order lines minimum lines"""
        products= self.order_line.product_id.mapped('id')
        print(products)
        if self.premium and len(products) < self.value:
            raise UserError("Less than required order_line products")

        return super(saleOrder,self).action_confirm()
