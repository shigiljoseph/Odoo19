# -*- coding: utf-8 -*-

from odoo import fields,models

class BuyProduct(models.TransientModel):
    """Create wizard to buy product"""

    _name = 'buy.product'
    _description = 'Buy product'

    product_template_id = fields.Many2one('product.template')
    name = fields.Char(related='product_template_id.name')
    partner_id = fields.Many2one('res.partner')
    price = fields.Float(related='product_template_id.list_price')
    quantity = fields.Integer()



    def action_buy(self):
        """Create sale order and invoice for the product"""
        quotation = self.env['sale.order'].search([ ('partner_id', '=', self.partner_id.id),
                                                    ('state', '=', 'draft')],limit=1)
        if quotation :
            quotation.write({
                'order_line': [
                    fields.Command.create({
                        'product_id': self.product_template_id.product_variant_id.id,
                        'product_uom_qty': self.quantity,
                        'price_unit': self.price,
                    }),
                ],
            })

        else:
            quotation = self.env['sale.order'].create({
                'partner_id': self.partner_id.id,
                'order_line': [
                    fields.Command.create({
                        'product_id':self.product_template_id.product_variant_id.id,
                        'product_uom_qty': self.quantity,
                        'price_unit': self.price,
                    }),
                ],
            })

        quotation.action_confirm()
        invoice = quotation._create_invoices(quotation.order_line)
        invoice.action_post()




