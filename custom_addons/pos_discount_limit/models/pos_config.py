# -*- coding: utf-8 -*-

from odoo import fields,models


class PosConfig(models.Model):
    """Load fields to pos.config"""
    _inherit = 'pos.config'

    product_category_ids = fields.Many2many(
        'pos.category',
        'pos_category_limit_rel',
        'pos_id',
        'category_id',
    )
    limit = fields.Float(
        string="Discount Limit",
    )


