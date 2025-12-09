# -*- coding: utf-8 -*-

from odoo import fields,models
from odoo.exceptions import ValidationError, UserError


class PurchaseOrder(models.Model):
    """To add last purchased date and validation for vendor"""
    _inherit = 'purchase.order'

    def button_confirm(self):
        """Inherit Button confirm """
        res = super(PurchaseOrder, self).button_confirm()

        purchase_order = self.env['purchase.order'].sudo().search(
            [('partner_id', '=', self.partner_id.id)], limit=1)

        print(purchase_order)

        if purchase_order:
            approve_date = fields.Date.from_string(purchase_order.date_approve)
            confirm_date = fields.Date.from_string(self.date_approve)
            print(confirm_date)
            date = fields.Date.from_string('2025-09-09')
            print(date)
            date_count = (confirm_date - date).days
            print(approve_date)

            invoices = self.env['account.move'].sudo().search([('partner_id', '=', self.partner_id),
                                            ('state', '=', 'posted'),('move_type', '=', 'in_invoice')])


            if len(invoices.filtered('payment_count')) != len(invoices):
                raise UserError('vendor have overdue')

            if date_count > 90:
                raise ValidationError('Vendor hasn’t supplied anything for more than 90 days')

            self.partner_id.last_reference_date = purchase_order.date_approve
        else:
            self.partner_id.last_reference_date = self.date_approve

        return res