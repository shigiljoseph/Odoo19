# -*- coding: utf-8 -*-

from odoo import fields,models

class SaleOrderLine(models.Model):
    """Add a new field to sale order line"""
    _inherit = 'sale.order.line'

    milestone = fields.Integer()