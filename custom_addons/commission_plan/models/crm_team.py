# -*- coding: utf-8 -*-

from odoo import api,fields,models

class CrmTeam(models.Model):
    """Add a field in crm.team"""

    _inherit = 'crm.team'

    commission_id = fields.Many2one('crm.commission')

    @api.onchange('commission_id')
    def _onchange_commission(self):
        """To set the commission plan on the crm.team.members model"""
        self.crm_team_member_ids.write({'commission_id' : self.commission_id})
        for record in self.crm_team_member_ids:
            record.user_id.commission_id = self.commission_id