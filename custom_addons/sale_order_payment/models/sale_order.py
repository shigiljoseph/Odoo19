# -*- coding: utf-8 -*-

from odoo import fields, models


class saleOrderPayment(models.Model):
    """Make payment from the sale order"""
    _inherit = 'sale.order'

    def action_create_payment(self):
        """Confirm quotation and create invoice and payment"""
        self.action_confirm()
        # invo = self.env['sale.advance.payment.inv'].sudo().create([{
        #             'advance_payment_method': 'delivered',
        #             'sale_order_ids': [fields.Command.link(self.id)],
        #         }]).create_invoices()
        invoice = self._create_invoices(self.order_line)

        print("invo", invoice)
        # invoice = self.env['account.move'].sudo().browse(invo['res_id'])
        invoice.action_post()
        self.env['account.payment.register'].with_context(active_model='account.move', active_ids=invoice.ids).create({
            'payment_date': invoice.date,
        }).action_create_payments()




