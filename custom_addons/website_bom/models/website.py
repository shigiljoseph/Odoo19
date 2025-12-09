# -*- coding: utf-8 -*-

from odoo import models, fields


class Website(models.Model):
    """To add a field in website model to store the  selected
     products in settings """

    _inherit = 'website'

    product_ids = fields.Many2many(
        'product.product',
        'website_product_bom_rel',
        'website_id',
        'product_id',
    )