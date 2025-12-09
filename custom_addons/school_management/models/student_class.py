# -*- coding: utf-8 -*-

from odoo import models,fields

class StudentClass(models.Model):

    """Holds the name and department of ach class"""

    _name = "student.class"
    _description = "Student Class"
    _inherit = ['mail.thread']
    _sql_constraints = [('Unique_name','UNIQUE(name)',"Class name must be unique")]


    name = fields.Char(string="Name" , required=True, tracking=True)
    department_id = fields.Many2one("school.department", string='Department', tracking=True)
    hod = fields.Char('HOD',related='department_id.hod_id.name')
    student_ids = fields.One2many('student.registration', 'current_class_id')
    school_id = fields.Many2one("res.company", default=lambda self: self.env.company, string="School")
