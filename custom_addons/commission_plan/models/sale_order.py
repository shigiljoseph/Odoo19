# -*- coding: utf-8 -*-
from dateutil.utils import today

from odoo import api,fields,models


class SaleOrder(models.Model):
    """To add a commission in sale order and calculate according to the sales persons commission plan """
    _inherit = 'sale.order'

    commission = fields.Float(default=0.0)

    def _action_confirm(self):
        """To calculate commission based on the commission plan by overriding action_confirm"""
        res = super()._action_confirm()

        self.commission = 0.0
        total_commission = 0.0
        today = fields.Date.today()

        commission_id = self.user_id.commission_id

        if not commission_id:
            commission_id = self.team_id.commission_id

            if not commission_id:
                return res

        if commission_id.from_date <= self.date_order.date() and commission_id.to_date >= self.date_order.date():
            commission_type = commission_id.type


            if commission_type == 'product_wise':

                commission_rules = self.user_id.commission_id.product_wise_ids

                for rec in self.order_line:
                    product_rule = commission_rules.filtered(
                        lambda r: r.product_id.id == rec.product_id.id
                    )
                    if not product_rule:
                        pass

                    line_commission = rec.price_subtotal * (product_rule.rate / 100.0)

                    if line_commission > product_rule.max_commison_amount:
                        line_commission = product_rule.max_commison_amount

                    total_commission += line_commission

                self.commission = total_commission

            elif commission_type == 'revenue_wise':

                commission_rules = self.user_id.commission_id.revenue_wise_ids

                if not commission_rules:
                    pass

                if self.user_id.commission_id.revenue_type == 'straight':


                    rule = commission_rules.filtered(
                        lambda x: x.from_amount <= self.amount_total and x.to_amount >= self.amount_total
                    )
                    if not rule:
                        rule = commission_rules.filtered(
                            lambda x: x.to_amount <= self.amount_total).sorted(reverse=True)[0:1]
                    if rule.to_amount > self.amount_total:
                        self.commission = self.amount_total * (rule.rate / 100.0)
                    else:
                        self.commission = rule.to_amount * (rule.rate / 100.0)

                elif self.user_id.commission_id.revenue_type == 'graduated':

                    total_commission = 0.0
                    rule_commission = 0.0
                    amount = 0

                    for r in commission_rules:
                        compute_amount = r.to_amount - amount
                        if compute_amount > (self.amount_total - amount):
                            rule_commission = (self.amount_total - amount) * (r.rate / 100)
                            total_commission += rule_commission
                            break
                        else:
                            rule_commission = compute_amount * (r.rate / 100)
                            total_commission += rule_commission
                        amount = r.to_amount

                    self.commission = total_commission

                if self.commission :
                    if self.user_id:
                        self.user_id.write({
                            'commission_history_ids': [
                                fields.Command.create({
                                    'sale_order_id': self.id,
                                    'commission_id': commission_id.id,
                                    'date': self.date_order,
                                    'commission': self.commission,
                                })
                            ]
                        })
                    else:
                        self.team_id.user_id.write({
                            'commission_history_ids': [
                                fields.Command.create({
                                    'sale_order_id': self.id,
                                    'commission_id': commission_id.id,
                                    'date': self.validity_date,
                                    'commission': self.commission,
                                })
                            ]
                        })

        return res


