# -*- coding: utf-8 -*-

from odoo import fields,models
from odoo.exceptions import UserError


class AccountMove(models.Model):

    _inherit = 'account.move'

    def action_sale(self):
        if not self.partner_id or not self.invoice_line_ids:
            raise UserError('Required partner and order lines')
        if self.move_type == 'out_invoice':
            sale_order = self.env['sale.order'].create({
                'partner_id': self.partner_id.id,
                'date_order': self.date,
                'order_line': [
                    fields.Command.create({
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.quantity,
                        'price_unit': line.price_unit,
                        'tax_ids': line.tax_ids
                    }) for line in self.invoice_line_ids
                ]
            })
            sale_order.action_confirm()


            if self.sale_order_count == 0:
                self.invoice_origin = sale_order.name
                for line in self.invoice_line_ids:
                    so_line = sale_order.order_line.filtered(lambda l: l.product_id == line.product_id)
                    if so_line:
                        line.sale_line_ids = [fields.Command.link(so_line.id)]








