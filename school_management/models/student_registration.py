# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError


class StudentRegistration(models.Model):
    """Holds the basic information about the student for registration"""

    _name = "student.registration"
    _description = "Registration"
    _rec_name = "first_name"
    _inherit = ['mail.thread']
    _sql_constraints = [('Unique_admission_no','UNIQUE(admission_no)','Admission number should be unique'),
                        ('Unique_adhar_no', 'UNIQUE(adhar_no)', 'Adhar number should be unique')
                        ]

    first_name = fields.Char(required=True)
    last_name = fields.Char()
    father = fields.Char()
    mother = fields.Char()
    c_address = fields.Text(string="Communication Address")
    same_as_c_address = fields.Boolean(string="Same as Communication Address", default=False)
    p_address = fields.Text(string="Permanent Address ")
    email = fields.Char(required=True)
    phone = fields.Char(required=True)
    dob = fields.Date()
    gender = fields.Selection([('male', "Male"), ('female', 'Female'), ('other', 'Other')], default='male')
    reg_date = fields.Date(string='Registration Date', default=fields.Date.today())
    photo = fields.Char("Photo")
    previous_dep_id = fields.Many2one("school.department", string="Previous academic department")
    previous_class_id = fields.Many2one('student.class', string="Previous class")
    tc = fields.Binary()
    age = fields.Integer(compute="_compute_age",store=True)
    adhar_no = fields.Char(string='Aadhaar number')
    sequence = fields.Char(string='Sequence', readonly=True, tracking=True, copy=False,
                            default=lambda self: self.env[ 'ir.sequence'].next_by_code('registration.model'))

    status = fields.Selection([('draft', 'Draft'), ('cancel', 'Canceled'), ('reg', 'Registered')],
                            default='draft' , tracking=True)
    admission_no = fields.Char('Admission Number',readonly=True, tracking=True, copy=False)
    school_id = fields.Many2one("res.company", default= lambda self: self.env.company, string="School")
    club_ids = fields.Many2many('school.club',string="Club")
    exam_ids = fields.Many2many('student.exam')
    current_class_id = fields.Many2one('student.class' , string='Class', required=True)
    leave_ids = fields.One2many("student.leave","student_id")
    attendance = fields.Boolean(default=False)
    user_id = fields.Many2one('res.users')
    is_web_created = fields.Boolean(default=False)


    @api.onchange("same_as_c_address")
    def _onchange_same_as_c_address(self):
        """Set the permanent address same as current address """
        print(self.user_id)
        if self.same_as_c_address:
            self.p_address = self.c_address


    @api.depends("dob")
    def _compute_age(self):
        """Compute the age of the student based on the Date of Birth"""
        for record in self:
            today = fields.Date.today()
            record.age = relativedelta(today, record.dob).years


    def action_cancel(self):
        """Change the status to cancel"""
        self.status='cancel'



    def action_register(self):
        """Change the status to registered, generates a admission number and create a new user with student details"""
        self.write({'status' : 'reg' ,
                    'admission_no' : self.env['ir.sequence'].next_by_code('admission.model')
                  })


    def action_create_user(self,record):
        """Create a new user and send the username and password"""
        existing_user = self.env['res.users'].search([('login', '=', record.email)], limit=1)
        if not existing_user:
            self.user_id = self.env['res.users'].create({
                'name': record.first_name,
                'login': record.email,
                'email': record.email,
                'phone': record.phone,
                'group_ids': [fields.Command.set([self.env.ref('school_management.student_group_students').id,self.env.ref('base.group_user').id])],
                'password': record.email,
            })

            template = self.env.ref('school_management.email_template_user_invitation')
            template.send_mail(
                record.id,
                email_values = {'email_to': record.email},
                force_send = True
            )
        else:
            raise UserError("Existing mail use another")


    @api.constrains("previous_class_id")
    def _check_validation(self):
        """Validate the entered previous class and the department matches"""
        if self.previous_dep_id != self.previous_class_id.department_id :
            raise UserError(self.env._("Previous class doesn't match"))

