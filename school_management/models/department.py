# -*- coding: utf-8 -*-

from odoo import models,fields

class Department(models.Model):
    """holds the name and HOD incharge of a department """

    _name = "school.department"
    _description = "Departments"
    _inherit = ['mail.thread']
    _sql_constraints = [('Unique_name','UNIQUE(name)', "Department name must be unique")]

    name = fields.Char(required=True, tracking=True)
    hod_id = fields.Many2one("res.partner", String="Head of the department ", tracking=True)
    school_id = fields.Many2one("res.company", default=lambda self: self.env.company)
