# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    """Validate Internal transfer"""
    _inherit = 'stock.picking'

    def button_validate(self):
        """Check same user validating transfer"""
        if self.create_uid.id == self.env.user.id:
            raise UserError('Two step validation need')

        return super(StockPicking,self).button_validate()
