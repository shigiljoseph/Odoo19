# -*- coding: utf-8 -*-

from odoo import fields,models


class ResUsers(models.Model):
    """Add a field in user model"""
    _inherit = 'res.users'

    menus_ids = fields.Many2many('ir.ui.menu')

