# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json


class WebFormController(http.Controller):
    @http.route('/student_leave', auth='public', website=True)
    def display_web_form(self, **kwargs):
        students = self.env['student.registration'].search([('status', '=', 'reg')])
        return request.render('school_management.student_leave_form_template', {
            'students': students,
        })

    @http.route('/get_student_class/<int:student_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_student_class(self, student_id, **kwargs):
        student = request.env['student.registration'].sudo().browse(int(student_id))
        return json.dumps({'class_id': student.current_class_id.id, 'class_name': student.current_class_id.name})


    @http.route('/submit/leave', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def handle_web_form_submission(self, **post):
        """Create the student leave record"""

        request.env['student.leave'].sudo().create({
            'student_id': int(post.get('student_id')),
            'student_class_id': int(post.get('student_class_id')),
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
            'half_day': bool(post.get('half_day')),
            'reason': post.get('reason'),
        })
        return request.redirect('/contactus-thank-you')