# -*- coding: utf-8 -*-
from email.policy import default

from odoo import fields,models

class CrmCommission(models.Model):
    """To create commission plan"""

    _name = 'crm.commission'
    _description = 'crm commission'
    _inherit = ['mail.thread']

    name = fields.Char()
    active = fields.Boolean(default=True)
    from_date = fields.Date()
    to_date = fields.Date()
    type = fields.Selection([('product_wise', 'Product wise'), ('revenue_wise', 'Revenue wise')])
    revenue_type = fields.Selection([('straight', 'Straight'),('graduated','Graduated')],
                                    string="Revenue Type", default='straight')
    product_wise_ids = fields.One2many('product.wise.commission',
                                       'commission_id')
    revenue_wise_ids = fields.One2many('revenue.wise.commission',
                                       'commission_id')



class ProductWiseCommission(models.Model):
    """Product wise commission type model"""

    _name = 'product.wise.commission'
    _description = 'Product wise commission'

    commission_id = fields.Many2one('crm.commission')
    product_category_id = fields.Many2one('product.category')
    product_id = fields.Many2one('product.product')
    rate = fields.Float(string="Rate(%)")
    max_commison_amount = fields.Float()


class RevenueWiseCommission(models.Model):
    """Revenue wise commission type model"""

    _name = 'revenue.wise.commission'
    _description = 'Revenue wise commission'

    commission_id = fields.Many2one('crm.commission')
    sequence = fields.Char()
    from_amount = fields.Float(string='From Amount')
    to_amount = fields.Float(string='To Amount')
    rate = fields.Float(string="Rate(%)")