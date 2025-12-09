from email.policy import default

from odoo import fields,models

class CommissionHistory(models.Model):
    """Model for storing the commission history of users"""
    _name = 'commission.history'
    _description = 'Commission history'

    sale_order_id = fields.Many2one('sale.order')
    commission_id = fields.Many2one('crm.commission',ondelete='restrict')
    date = fields.Date()
    commission = fields.Float()
    user_id = fields.Many2one('res.users')
