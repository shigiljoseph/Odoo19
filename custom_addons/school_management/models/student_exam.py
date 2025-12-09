# -*- coding: utf-8 -*-

from odoo import fields,models

class StudentExam(models.Model):
    """To assign and create exam for students"""
    _name = "student.exam"
    _description = "Student Exam"
    _rec_name = "name"
    _inherit = ['mail.thread']

    name = fields.Char( tracking=True, required=True)
    class_id = fields.Many2one('student.class',
                               tracking=True,
                               string="class",
                               required=True)
    papers_ids = fields.One2many(comodel_name='exam.paper',
                                inverse_name='exam_id',
                                string="Papers",
                                copy=True)
    state = fields.Selection([('draft','Draft'), ('assign','Assigned'), ('cancel', 'Canceled')],
                              default='draft', tracking=True)
    school_id = fields.Many2one("res.company", default=lambda self: self.env.company)

    def action_assign(self):
        """Change state and assign the exams"""
        self.state = "assign"
        self.class_id.student_ids.write({'exam_ids': [fields.Command.link(self.id)]})


    def action_cancel(self):
        """Change state to canceled"""
        self.state = 'cancel'
        self.class_id.student_ids.write({ 'exam_ids': [fields.Command.unlink(self.id)] })


class ExamPaper(models.Model):
    """Model to hold the details about subject """
    _name = 'exam.paper'
    _rec_name = 'subject_id'
    _description = "Exam Paper"

    subject_id = fields.Many2one('subjects', string="Subject")
    pass_mark = fields.Integer()
    max_mark = fields.Integer()
    exam_id = fields.Many2one('student.exam')


