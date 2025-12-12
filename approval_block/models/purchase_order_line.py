from odoo import api,fields,models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'


    new_order_id = fields.Many2one('purchase.order')
    visible = fields.Boolean(compute='_compute_state',store=True)

    @api.depends('new_order_id')
    def _compute_state(self):
        for rec in self:
            if rec.new_order_id.state != 'draft':
                rec.visible = True
            else:
                rec.visible = False

    def action_add_line(self):
        self.new_order_id.write({"order_line": [fields.Command.create({
            'product_id': self.product_id.id,
            'product_uom_qty': self.product_uom_qty,
            'price_unit': self.price_unit,
            'tax_ids': self.tax_ids
        })]
        })
        self.visible = True
