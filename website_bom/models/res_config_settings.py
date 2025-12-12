# -*- coding: utf-8 -*-

from odoo import fields, models, api
from ast import literal_eval


class WebsiteSettings(models.TransientModel):
    """To add a field in website settings"""

    _inherit = 'res.config.settings'

    bom_active = fields.Boolean(config_parameter='website_bom.bom_active')
    product_ids = fields.Many2many(
        related='website_id.product_ids',
        string='Products with BoM',
        domain=[('bom_ids', '!=', False)],
        readonly=False
    )

    @api.onchange('bom_active')
    def _onchange_bom_active(self):
        if not self.bom_active:
            self.write({'product_ids': [fields.Command.clear()]})


    @api.model
    def get_values(self):
        res = super().get_values()
        product_ids = self.env['ir.config_parameter'].sudo().get_param('website_bom.product_ids')
        res.update({
            'product_ids': [fields.Command.set(literal_eval(product_ids))] if product_ids else [],
        })
        return res

    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].sudo().set_param('website_bom.product_ids', self.product_ids.ids)
