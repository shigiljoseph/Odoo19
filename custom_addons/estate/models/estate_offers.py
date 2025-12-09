from email.policy import default

from dateutil.relativedelta import relativedelta

from odoo import models,fields,api
from odoo.exceptions import ValidationError


class EstateOffers(models.Model):
     _name="estate.offer"
     _description = "Estate offer"
     _rec_name = "partner_id"
     _order = 'price desc'
     _sql_constraints = [('price','CHECK(price >0)','price should be positive')]

     property_type_ids = fields.Many2one('property_models', string="Property Type")
     price = fields.Float(string="Price")
     partner_id = fields.Many2one('res.partner',string="Partner")
     offer_id= fields.Many2one('test_model')
     status = fields.Selection([('yes','Accepted'),('no','Rejected'),('nill','')],default='nill')
     date = fields.Date(
         default=lambda self: fields.Date.today() + relativedelta(months=3),
         readonly=True,
         store=True, string="Staring Date"
     )
     validity = fields.Integer(default=7,string='Validity')
     date_deadline = fields.Date(compute='_date_deadline', inverse='_deadline_inverse', store=True,string='Dead Line')

     def accept_offer(self):
         self.status='yes'
         self.offer_id.buyer_id=self.partner_id
         self.offer_id.selling_price=self.price

         # @api.constrains("selling_price")
         # def _constraint_selling_price(self.offer_id):
         #     for record in self:
         if self.price < ((self.offer_id.Expected_Price * 90) / 100):
             raise ValidationError("The selling price cannot be sless than 90% of expected price")

     def cancel_offer(self):
         self.status='no'



     @api.depends("validity")
     def _date_deadline(self):
         for record in self:
             record.date_deadline = record.date + relativedelta(days=record.validity)

     @api.depends('date_deadline', 'date')
     def _deadline_inverse(self):
         for record in self:
             if record.date and record.date_deadline:
                 if record.date > record.date_deadline:
                     record.validity = 0
                 else:
                     delta = record.date_deadline - record.date
                     print(delta)
                     record.validity = delta.days
             else:
                 record.validity = 0








