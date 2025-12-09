# -*- coding: utf-8 -*-

from odoo import api,fields,models


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product",
        change_default=True, ondelete='restrict', index='btree_not_null',
        domain="[('sale_ok', '=', True), ('id', 'in', parent.product_ids)]",
        check_company=True)

    def _domain_product_id(self):
        res = super()._domain_product_id()

        return res