
# -*- coding: utf-8 -*-
import base64
from datetime import timedelta
from odoo import  fields, models
from odoo.tools import date_utils


class SaleReport(models.Model):
    """To Send sale report for the selected customers based on selected values"""
    _name = 'customer.sale.report'
    _description = 'Customer Sale Report'

    name = fields.Char(default='Sales Report')
    customer_ids = fields.Many2many("res.partner", string='Customers', required=True)
    sales_team_id = fields.Many2one('crm.team', string='Sales Team', required=True)
    type = fields.Selection([('Weekly', 'Weekly'), ('Monthly', 'Monthly')], required=True)
    from_date = fields.Date(string='From', required=True)
    to_date = fields.Date(string='To', required=True)
    status = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('Cancel', 'Cancel')],
                              default='draft')


    def action_confirm(self):
        """Confirm the record and create ir.cron record """
        self.status = 'confirmed'


    def action_cancel(self):
        """Change the status the canceled"""
        self.status = 'Cancel'


    def action_sent_report(self):
        """To send mail based on the ir.cron and attach the pdf report"""

        datas = self.search([])
        today = fields.Date.today()

        for data in datas:
            if today > data.to_date or today < data.from_date:
                return

            if data.type == 'Weekly':
                days_since_monday = today.weekday()
                period_end = today + timedelta(days=(5 - days_since_monday))
                period_start = period_end - timedelta(days=6)

                if today.strftime('%Y-%U') == data.from_date.strftime('%Y-%U'):
                    period_start = data.from_date

            elif data.type == 'Monthly':
                period_start, period_end = date_utils.get_month(today)
                if today.strftime('%Y-%m') == data.from_date.strftime('%Y-%m'):
                    period_start = data.from_date

            if period_end > data.to_date or period_start < data.from_date or period_end != today:
                continue

            sale_team = data.sales_team_id.id

            for cust in data.customer_ids:
                query = """
                            SELECT so.name, so.date_order, so.amount_total, rp.name as customer_name
                            FROM sale_order so
                            JOIN res_partner rp ON so.partner_id = rp.id
                            WHERE so.partner_id = %s AND so.team_id = %s         
                              AND so.date_order BETWEEN %s AND %s 
                        """
                self.env.cr.execute(query, (cust.id,sale_team, period_start, period_end))
                results = data.env.cr.dictfetchall()

                if not results:
                    return

                report_data = {
                    'cust': cust,
                    'report_type': data.type,
                    'from_date': period_start,
                    'to_date': period_end,
                    'sale_orders': results,
                }

                report_template = self.env.ref('customer_sales_report.action_customer_sale_report')

                pdf_content, _ = self.env['ir.actions.report'].sudo()._render_qweb_pdf(
                    report_template, data=report_data)
                pdf_data = base64.b64encode(pdf_content)


                attachment = self.env['ir.attachment'].create({
                    'name': f'Sales_Report_{cust.name}.pdf',
                    'type': 'binary',
                    'datas': pdf_data,
                    'mimetype': 'application/pdf',
                    'res_model': self._name,
                    'res_id': data.id,
                })

                email_values = {
                    'email_to': cust.email,
                    'attachment_ids': [fields.Command.link(attachment.id)],
                }
                template = self.env.ref('customer_sales_report.email_template_customer_report')
                template.send_mail(data.id, email_values=email_values, force_send=True)


