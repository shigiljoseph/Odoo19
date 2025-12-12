# -*- coding: utf-8 -*-

from odoo import api,fields,models

class PurchaseOrder(models.Model):
    """To add a field block and set value for it in purchase order"""
    _inherit = 'purchase.order'


    block_id = fields.Many2one('approval.block',string="Block Limit",
                               compute='_compute_block', inverse='_inverse_block')




    existing_lines = fields.Many2many('purchase.order.line',compute='_compute_records')

    @api.depends('partner_id')
    def _compute_records(self):
        for rec in self:
            rec.existing_lines = self.env['purchase.order.line'].search([
                ('partner_id', '=', rec.partner_id),('state', '=', 'purchase')],limit=20)
            [line.write({
                    'new_order_id': rec.id
            })for line in rec.existing_lines]

    def action_add_lines(self):
        self.write({"order_line":[fields.Command.create ({
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'price_unit': line.price_unit,
                'tax_ids': line.tax_ids
            }) for line in self.existing_lines]})




    @api.depends('amount_total')
    def _compute_block(self):
        """Compute the block value"""
        for record in self:
            matching_block = self.block_id.search(
                [('block', '<=', record.amount_total)],
                order='block desc',
                limit=1
            )
            record.block_id = matching_block.id

    def _inverse_block(self):
        """Enable the Block field editable"""
        pass



