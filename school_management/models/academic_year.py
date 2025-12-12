# -*- coding: utf-8 -*-
from odoo import fields, models


class AcademicYear(models.Model):
    """Holds academic year"""

    _name = "academic.year"
    _description = "Academic year"
    _sql_constraints = [('Unique_year','UNIQUE(year)',"Year name must be unique")]

    year = fields.Char(required=True)
    school_id = fields.Many2one("res.company", default=lambda self: self.env.company)
