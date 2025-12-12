# -*- coding: utf-8 -*-
from email.policy import default

from odoo import api,fields,models

class ResUsers(models.Model):
    """To add a field in crm.team.member"""

    _inherit = ['res.users','mail.thread']

    commission_id = fields.Many2one('crm.commission',string='commission' )
    month_commission = fields.Float(tracking=True)
    total = fields.Float(compute='_compute_total_commission')
    commission_history_ids = fields.One2many('commission.history', 'user_id',tracking=True)
    commission_count = fields.Integer()

    @api.depends('commission_history_ids')
    def _compute_total_commission(self):
        """Compute the monthly and total commission"""
        for record in self:
            current_month = fields.Date.today()

            record.total = sum(record.commission_history_ids.mapped('commission'))
            record.month_commission = sum(record.commission_history_ids.filtered(lambda x:x.date.month == current_month.month).mapped('commission'))

            record.commission_count = len(record.commission_history_ids)

    def action_commission(self):
        """To view the commission of user"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Commission',
            'view_mode': 'list',
            'res_model': 'commission.history',
            'domain': [('user_id', '=', self.id)],
            'context': {
                'create':False,
                'search_default_commission_date': 1
            }
        }

