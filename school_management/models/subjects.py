# -*- coding: utf-8 -*-
from email.policy import default

from odoo import models,fields


class Subjects(models.Model):
    """Holds the name and department of each subject"""

    _name = "subjects"
    _description = "Subjects"
    _inherit = ['mail.thread']

    name = fields.Char(String="Name", tracking=True)
    department_id = fields.Many2one("school.department",string="Department", tracking=True)
    school_id = fields.Many2one("res.company", default= lambda self: self.env.company)

    purchase_id = fields.Many2one("purchase.order")
    product_id = fields.Many2one('product.product')
    price = fields.Float()


    def action_confirm(self):
        """Confirm PO"""

        if self.purchase_id.state == 'draft':
            self.purchase_id.button_confirm()


        # for rec in self.purchase_id.partner_id.property_product_pricelist.item_ids:
        #     start_date = rec.date_start.date() if rec.date_start else self.today
        #     end_date = rec.date_end.date() if rec.date_end else self.today
        #
        #     if rec.product_tmpl_id:
        #         if rec.product_id:
        #             if rec.product_id == self.product_id:
        #                 self.price = rec.fixed_price
        #                 break
        #         elif (rec.product_tmpl_id == self.product_id.product_tmpl_id and
        #               start_date <= self.purchase_id.date_approve and end_date >= self.purchase_id.date_approve) :
        #             self.price = rec.fixed_price
        #     elif rec.categ_id:
        #         if self.product_id.categ_id == rec.categ_id:
        #             self.price = rec.fixed_price
        #     else:
        #         self.price = rec.fixed_price

        sale = self.env['sale.order'].search([],limit=1)
        price_unit = sale.partner_id.property_product_pricelist._get_product_price(
            product=self.product_id,
            quantity=1.0,
        )
        self.price=price_unit