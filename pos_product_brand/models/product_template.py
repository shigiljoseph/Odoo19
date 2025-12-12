# -*- coding: utf-8 -*-

from odoo import api,fields,models

class ProductTemplate(models.Model):
    """Add a field brand in product template """

    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand')

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data += ['brand_id']
        return data