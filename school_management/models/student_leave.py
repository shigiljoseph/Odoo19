# -*- coding: utf-8 -*-

from datetime import timedelta, date

from odoo import fields, models, api
from odoo.exceptions import UserError


class StudentLeave(models.Model):
    """Holds the details of student leaves"""

    _name = 'student.leave'
    _description = 'student leaves'
    _rec_name = 'student_id'
    _inherit = ['mail.thread']

    student_id = fields.Many2one('student.registration', string='Student', tracking=True, required=True)
    student_class_id = fields.Many2one('student.class', string='Class', tracking=True, required=True,
                                       related="student_id.current_class_id")
    start_date = fields.Date()
    end_date = fields.Date()
    half_day = fields.Boolean(tracking=True)
    reason = fields.Text(required=True)
    total_days = fields.Float(compute="_compute_total_days", inverse='_inverse_total_days', store= True)
    school_id = fields.Many2one("res.company", default= lambda self: self.env.company)


    @api.onchange("half_day")
    def _onchange_half_day(self):
        """If half_day is enabled the start date and end date become same and set total days """
        if self.half_day:
            self.total_days = 0.5
            self.end_date = self.start_date


    @api.constrains('end_date','half_day')
    def _check_date(self):
        """Check the start date is greater than the end date and start date and end date are same for the half day"""
        if self.end_date < self.start_date :
            raise UserError("Start date must be greater than end date")
        if(self.start_date < date.today()):
            raise UserError("Date can't be past date ")



    @api.depends("start_date", "end_date")
    def _compute_total_days(self):
        """To compute the total number of days excluding sundays and saturdays"""
        for record in self:
            if record.start_date and record.end_date and record.start_date <= record.end_date:
                day_count = 0
                current_day = record.start_date

                while current_day <= record.end_date:
                    if current_day.weekday() < 5:
                        day_count += 1
                    current_day += timedelta(days=1)

                record.total_days = day_count

                if record.half_day:
                    record.total_days = 0.5
            else:
                record.total_days = 0


    def _inverse_total_days(self):
        """To change the end date if total days is changed """
        for record in self:
            record.end_date = record.start_date + timedelta(days = record.total_days)

    def _student_attendance_check(self):
        """Check student is on leave """
        students = self.env['student.registration'].search([])
        students.write({"attendance": False})
        today = fields.Date.today()
        self.search([('start_date','<=',today),('end_date','>=',today)]).mapped("student_id").write({"attendance": True})
        print(self.search([('student_id.attendance','=',True)]))


