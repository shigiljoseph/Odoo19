from dateutil.relativedelta import relativedelta
from png import Default
from reportlab.graphics.transform import inverse

from odoo.api import readonly
from odoo.exceptions import UserError, ValidationError
from odoo.tools import date_utils


from odoo import fields, models,api


class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model"
    _order = 'name desc'
    _sql_constraints = [
        ('check_price', 'CHECK(selling_price > 0 AND Expected_Price>0)',
         'The selling price o should be a positive value.')
    ]

    name = fields.Char(required=True,String="Name")
    tag = fields.Many2many('property.tags', string="Tags")
    sales_person=fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    property_type=fields.One2many('_type','type_id',string='Type')
    offer_ids=fields.One2many( 'estate.offer','offer_id')
    description= fields.Text()
    post_code= fields.Char()
    date = fields.Date(
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        readonly=True,
        store=True
    )
    Expected_Price= fields.Float(readonly=True,default=10000,copy=False)
    bedrooms=fields.Integer()
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    buyer_id=fields.Many2one('res.partner',string='Buyer')
    garden= fields.Boolean()
    garden_area=fields.Integer(default=0)
    garden_orientation=fields.Selection([('manual', ' '), ('f', 'North'), ('fr', 'South')], default='manual')
    total_area= fields.Float(compute="_compute_total",inverse='_inverse_total',store=True)

    best_price = fields.Float(compute='_compute_bestprice',store=True)

    status=fields.Selection(string='Status', required=True, readonly=True, copy=False, selection=[
            ('New', 'New'),
            ('Canceled', 'Canceled'),
            ('Sold', 'Sold'),
        ], default='New')

    selling_price = fields.Float()





    @api.onchange("garden")
    def _garden_change(self):
        if self.garden==True:
            self.garden_area=10
            self.garden_orientation='f'
        else:
            self.garden_area = 0
            self.garden_orientation = 'manual'


    @api.depends("offer_ids")
    def _compute_bestprice(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            if prices:
                record.best_price = max(prices)
            else:
                record.best_price = 0.0


    @api.depends("garden_area","living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("garden_area", "living_area")
    def _inverse_total(self):
        for record in self:
            record.garden_area = record.total_area - record.living_area

    def sold(self):
        for record in self:
            if record.status =='New' :
                record.status='Sold'

            elif  record.status=='Sold':
                raise UserError(self.env._("Already sold"))
            else:
                raise UserError(self.env._("Canceled item can't be sold"))

        return True



    def canceled(self):
        for record in self:
            if record.status =='New' :
                record.status='Canceled'
            elif record.status=='cCanceled':
                raise UserError(self.env._("Already canceled"))
            else:
                raise UserError(self.env._("Sold item can't be canceled"))
        return True

    @api.model
    def delete(self, vals):
            if self.status=='New' or self.status=='Canceled':

                return super(TestModel,self).delete(vals)

class _property_Type(models.Model):
    _name = '_type'
    _description = 'property type'

    type_id=fields.Many2one('test_model')
    name=fields.Char()




