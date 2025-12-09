# -*- coding: utf-8 -*-

from odoo import fields,models

class ApprovalBlock(models.Model):
    _name = 'approval.block'
    _rec_name = 'block'
    _description = 'Approval Block'

    name = fields.Char()
    block = fields.Integer()

