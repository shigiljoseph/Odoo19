# -*- coding: utf-8 -*-

from odoo import api,fields,models


class TransferRequest(models.Model):
    """Make a request to transfer employee company"""
    _name = 'employee.transfer'
    _description = "Transfer Employee"
    _rec_name = 'name'
    _inherit =  ['mail.thread']

    emp_id = fields.Many2one('hr.employee', string='Employee Name',required=True, tracking=True)
    name = fields.Char(related='emp_id.name')
    date = fields.Date(default=fields.Date.today)
    company_id = fields.Many2one('res.company', string='Transfer From')
    transfer_cmp_id = fields.Many2one('res.company' ,string='Transfer To', required=True, tracking=True)
    status = fields.Selection([('draft','Draft'),('requested','Requested'),('done','Done')],default='draft'
                              , tracking=True)

    def action_request(self):
        """Action to change status to requested"""
        self.write({'status' : 'requested'})

    def action_done(self):
        """Action to make employee company transfer status to done """
        self.emp_id.write({
            'company_id': self.transfer_cmp_id.id
        })
        self.write({'status' : 'done'})

    @api.onchange('emp_id')
    def _onchange_emp_id(self):
        """Select the employees company """
        if self.emp_id:
            self.company_id = self.emp_id.company_id


