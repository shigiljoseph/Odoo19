# -*- coding: utf-8 -*-

from odoo import api,fields,models

class CrmTeamMembers(models.Model):
    """To add a field in crm.team.member"""

    _inherit = 'crm.team.member'

    commission_id = fields.Many2one('crm.commission', readonly=False )


