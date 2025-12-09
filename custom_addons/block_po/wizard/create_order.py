# -*- coding: utf-8 -*-

from odoo import api,fields,models

class createOrder(models.TransientModel):
    """Create wizard to create sale order"""

    _name = 'create.order'
    _description = 'create sale order'


    partner_id = fields.Many2one('res.partner')


    def action_create_order(self):
        active_ids = self.env.context.get('active_ids')
        selected_lines = self.env['sale.order.line'].browse(active_ids)

        order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'order_line': [fields.Command.create ({
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'price_unit': line.price_unit,
                'tax_ids': line.tax_ids
            }) for line in selected_lines]
        })

        print(order)
        return {'type': 'ir.actions.act_window_close'}





