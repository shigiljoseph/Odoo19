# -*- coding: utf-8 -*-

from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """Unlink the picking_ids"""
        res = super().action_confirm()
        self.picking_ids.unlink()
        return res


    def action_delivery(self):
        """To confirm the quotation"""
        self._action_confirm()

