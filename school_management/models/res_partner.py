# -*- coding: utf-8 -*-

from odoo import fields,models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    """Inherits the res.partner and add a field role"""
    _inherit = 'res.partner'

    role = fields.Selection([('student','Student'),('teacher','Teacher'),('office','Office Staff')])
    user_id = fields.Many2one('res.users')

    def action_create_user(self,record):
        existing_user = self.env['res.users'].search([('login', '=', record.email)], limit=1)
        if not existing_user:
            if record.role == 'teacher':
                self.user_id = self.env['res.users'].create({
                    'name': record.name,
                    'login': record.email,
                    'email': record.email,
                    'group_ids': [fields.Command.set([self.env.ref('school_management.student_group_students').id,self.env.ref('base.group_user').id])],
                    'partner_id':record.id,
                    'password': record.email,
                })

            if record.role == 'office':
                self.user_id = self.env['res.users'].create({
                    'name': record.name,
                    'login': record.email,
                    'email': record.email,
                    'group_ids': [fields.Command.set([self.env.ref('school_management.student_group_students').id,self.env.ref('base.group_user').id])],
                    'partner_id':record.id,
                    'role':'[group_user]',
                    'password': record.email,
                })

            template = self.env.ref('school_management.email_template_employee_invitation')
            template.send_mail(
                record.id,
                email_values={'email_to': record.email},
                force_send=True
            )
        else:
            raise UserError("Existing mail")