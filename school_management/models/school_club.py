# -*- coding: utf-8 -*-
from odoo import fields,models

class SchoolClub(models.Model):
    """Create club for the school and view the events by the club"""
    _name = "school.club"
    _description = "School clubs"
    _inherit = ['mail.thread']

    name = fields.Char(reuired=True)
    incharge_id = fields.Many2one("res.partner")
    color = fields.Integer(tracking=True)
    members_ids = fields.Many2many('student.registration', tracking=True)
    event_count = fields.Integer(string="Event", compute='_compute_event_count')
    school_id = fields.Many2one("res.company", default=lambda self: self.env.company)

    def _compute_event_count(self):
        """To count the number of events in the club"""
        for record in self:
            record.event_count = self.env['school.events'].search_count([('club_id', '=', self.id)])

    def action_events(self):
        """To view the events in the club"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Events',
            'view_mode': 'list',
            'res_model': 'school.events',
            'domain': [('club_id', '=', self.id)],
            'context': {'create':False}
        }

