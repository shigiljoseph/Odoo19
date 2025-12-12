# -*- coding: utf-8 -*-

from odoo import fields,models

class SaleOrder(models.Model):
    """Inherits teh sale.order and add a state admitted"""
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('admit', 'Admitted')])
