from enum import UNIQUE

from odoo import fields, models, api
from odoo.api import depends
from odoo.exceptions import UserError


class model(models.Model):
    _name = "property_models"
    _description = "Property types"
    _sql_constraints = [('Unique_type','UNIQUE(name)',"Property type already exist")]
    _order = 'name'

    name=fields.Char(required=True)
    offer_ids = fields.One2many("estate.offer", "property_type_ids", string="Offers")
    offer_count=fields.Float(compute="count")

    @api.depends("offer_ids")
    def count(self):
        for record  in self:
            record.offer_count=len(record.offer_ids)


