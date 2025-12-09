# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class WebFormController(http.Controller):
   @http.route('/student_registration', auth='public', website=True)
   def display_web_form(self):
       """Display form template"""
       print('innn')
       stud_class = request.env['student.class'].search([])
       return request.render('school_management.web_form_template',{'stud_class':stud_class,'page_name': 'student_registration'})

   @http.route('/student_list', auth='public', website=True)
   def display_student_list(self):
       """Display student_list"""
       student = request.env['student.registration'].search([('is_web_created','=',True)])
       return request.render('school_management.student_list', {'student': student , 'page_name': 'student_list'})

   @http.route("/student/<model('student.registration'):student>", type='http', auth='public', website=True)
   def student_edit_form(self, student=None):
       """Display the student details for edit"""
       stud_class = request.env['student.class'].search([])
       return request.render('school_management.form_template', {
           'student': student,
           'stud_class' : stud_class,
           'page_name': 'student_edit_form'
       })

   @http.route('/student_reg/<model("student.registration"):student>', type='http', auth='public', website=True)
   def student_reg_form(self, student=None, **kw):
       """Student Registration"""
       print(student)
       student.action_register()
       students = request.env['student.registration'].search([('is_web_created', '=', True)])
       return request.render('school_management.student_list', {'student': students,})


   @http.route('/student-thank-you', type='http', auth='public', website=True)
   def student_thank_page(self, student=None, **kw):
       """Thank you page"""
       print('tthh')
       return request.render('school_management.thank_you', {'student': student})

   @http.route('/webform/submit', type='http', auth='public', website=True, methods=['POST'], csrf=True)
   def handle_web_form_submission(self, **post):
       """Create the student record"""
       print('sdfuio')
       student = request.env['student.registration'].sudo().create({
           'first_name': post.get('first_name'),
           'last_name': post.get('last_name'),
           'phone': post.get('phone'),
           'email': post.get('email'),
           'gender' : post.get('gender'),
           'current_class_id': int(post.get('class_id')),
           'dob': post.get('dob'),
           'father': post.get('father_name'),
           'mother': post.get('mother_name'),
           'is_web_created' : True
       })

       return request.render('school_management.thank_you', {'student': student})


   @http.route('/edit_form/submit', type='http', auth='public', website=True, methods=['POST'], csrf=True)
   def handle_edit_form_submission(self, **post):
       """Edit the student record"""
       student_id = post.get('student_id')
       if student_id:
           request.env['student.registration'].sudo().browse(int(student_id)).write({
               'first_name': post.get('first_name'),
               'last_name': post.get('last_name'),
               'phone': post.get('phone'),
               'email': post.get('email'),
               'current_class_id': int(post.get('class_id')),
               'gender': post.get('gender'),
               'dob': post.get('dob'),
               'father': post.get('father'),
               'mother': post.get('mother'),
               'is_web_created' : True
           })
       return request.redirect('/student_list')
