# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    """To add a field in POS settings"""

    _inherit = 'res.config.settings'

    limit = fields.Float(related='pos_config_id.limit', readonly=False)

    product_category_ids = fields.Many2many(
        related='pos_config_id.product_category_ids', readonly=False
    )
    limit_active = fields.Boolean(config_parameter='website_bom.bom_active')

    @api.onchange('limit_active')
    def _onchange_limit_active(self):
        if not self.limit_active:
            self.update({'product_category_ids': [fields.Command.clear()]})
            self.update({'limit': 0})

