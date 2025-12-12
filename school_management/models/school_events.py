# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields, models, api
from odoo.exceptions import UserError


class SchoolEvents(models.Model):
    """Creates an event in school"""
    _name = "school.events"
    _description = "School Events"
    _inherit = ['mail.thread']

    name = fields.Char(required=True,tracking=True)
    club_id = fields.Many2one('school.club',tracking=True)
    start_date = fields.Date()
    end_date = fields.Date()
    status = fields.Selection([('draft','Draft'),('start','Start'),('end','Ended'),
                               ('cancel','Cancel')],default='draft')
    description = fields.Html()
    active = fields.Boolean(default=True)
    school_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    image = fields.Char("Photo")

    def action_start(self):
        """Change status to start"""
        self.status = 'start'


    def action_end(self):
        """Change status to end and set active"""
        self.write({'status' : 'end', 'active' : False})

    def action_cancel(self):
        """Change status to cancel"""
        self.status = 'cancel'

    def action_send_mail(self):
        """send mail to every employee"""
        template = self.env.ref('school_management.email_template_event_reminder')
        partners = self.env['res.partner'].search([('role','in', ['teacher', 'office'])])
        email_to = ','.join(partners.mapped('email'))
        template.send_mail(
                self.id,
                email_values = {'email_to': email_to},
                force_send = True
            )

    def _send_event_remainder(self):
        """Auto send email to employees before 2 days"""
        today = fields.Date.today()
        expected_date = today + timedelta(2)
        events = self.search([
            ('start_date', '=', expected_date),
        ])
        template = self.env.ref("school_management.email_template_event_reminder")
        partners = self.env['res.partner'].search([('role','in', ['teacher', 'office'])])
        email_to = ','.join(partners.mapped('email'))
        for event in events:
            template.send_mail(
                event.id,
                email_values={'email_to': email_to},
                force_send=True
            )

    def _end_events(self):
        """End events that have passed the end date"""
        now = fields.Datetime.now()
        self.search([
            ('end_date', '<', now),
            ('status', '!=', 'end')
        ]).write({'status': 'end', 'active': False})



    @api.constrains("end_date")
    def _check_dates(self):
        """Validate start date greater tan end date"""

        if self.end_date < self.start_date:
            raise UserError("End date must be greater than start date")


