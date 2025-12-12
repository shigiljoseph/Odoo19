# -*- coding: utf-8 -*-

from odoo import api,fields,models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    product_ids = fields.Many2many('product.product',string='Products')

