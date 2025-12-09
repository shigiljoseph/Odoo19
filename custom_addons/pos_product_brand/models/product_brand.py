# -*- coding: utf-8 -*-

from odoo import fields,models

class ProductBrand(models.Model):
    """Create brand for the product"""

    _name = "product.brand"
    _description = "Product brand"
    _inherit = ['pos.load.mixin']

    name = fields.Char()
