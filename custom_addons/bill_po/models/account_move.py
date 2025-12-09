# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for record in self:
            if record.move_type == 'in_invoice':
                purchase_order = self.env['purchase.order'].with_context(default_move_type='direct').create({
                    'partner_id': record.partner_id.id,
                    'date_order': record.date,
                    'order_line': [
                        fields.Command.create({
                            'product_id': line.product_id.id,
                            'product_uom_qty': line.quantity,
                            'price_unit': line.price_unit,
                            'tax_ids': line.tax_ids
                        }) for line in record.invoice_line_ids
                    ]
                })
                purchase_order.button_confirm()
                print('purchase_order',purchase_order)

                record.purchase_id = purchase_order.id

                match_lines = self.env['purchase.bill.line.match'].sudo().search([
                    ('partner_id', '=', self.partner_id.id)])

                print('match_lines',match_lines.display_name)

                match_lines.action_match_lines()

        return res

