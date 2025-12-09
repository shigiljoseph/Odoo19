# -*- coding: utf-8 -*-

from odoo import fields,models


class ResPartner(models.Model):
    """Add field in res.partner"""
    _inherit = 'res.partner'

    last_reference_date = fields.Date(default=fields.Date.today)
    premium = fields.Boolean()
    value = fields.Integer()


