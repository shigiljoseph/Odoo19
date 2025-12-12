# -*- coding: utf-8 -*-

from odoo import models


class IrUiMenu(models.Model):
    """Hide the menus"""
    _inherit = 'ir.ui.menu'

    def _filter_visible_menus(self):
        menus = super()._filter_visible_menus()
        user = self.env.user
        if user.menus_ids:
            return menus.filtered(lambda m: m.id not in user.menus_ids.ids)
        return menus