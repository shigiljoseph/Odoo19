# -*- coding: utf-8 -*-

import datetime
import io
import json
import xlsxwriter
from odoo import api,fields,models
from odoo.exceptions import UserError
from odoo.tools import json_default,date_utils


class EventInformation(models.TransientModel):
    """Create the wizard for the event report """
    _name = 'event.information'
    _description = 'event Information'

    period = fields.Selection([('day','Day'),('week','Weekly'),('month','Monthly'),('custom','Custom')], default='custom')
    from_date = fields.Date()
    to_date = fields.Date()
    club_id = fields.Many2one('school.club')

    def action_print_report(self):
        """Returns from ir.actions.report action"""

        from_date = self.from_date
        to_date = self.to_date
        club_id = self.club_id.id if self.club_id else None

        return self.env.ref('school_management.action_event_information_report').report_action(
            None,
            data={
                'from_date' : from_date ,
                'to_date' : to_date,
                'club_id' : club_id
            }
        )

    def action_xl_report(self):
        """Returns ir.actions.report action for creating xlsx report"""
        from_date = self.from_date
        to_date = self.to_date
        club_id = self.club_id.id if self.club_id else 0

        if from_date and to_date:
            if from_date > to_date:
                raise UserError('Invalid date range')

        params = """
                    SELECT
                           se.name,se.start_date, se.end_date,se.status,
                             sc.name as cname, rp.name as rname
                       FROM school_events se
                       JOIN school_club sc ON se.club_id = sc.id
                       JOIN res_partner rp ON sc.incharge_id = rp.id
                 """

        if club_id:
            print(club_id)
            if not from_date and to_date:
                query = params + """ WHERE (se.start_date <= %s OR se.end_date <= %s)  AND sc.id = %s"""
                self.env.cr.execute(query, (to_date, to_date, club_id))
                report = self.env.cr.dictfetchall()
            elif not to_date and from_date:
                query = params + """WHERE (se.start_date >= %s OR se.end_date >= %s)  AND sc.id = %s """
                self.env.cr.execute(query, (from_date, from_date, club_id))
                report = self.env.cr.dictfetchall()
            elif not to_date and not from_date:
                query = params + """ WHERE sc.id = %s"""
                self.env.cr.execute(query,(club_id,))
                report = self.env.cr.dictfetchall()
            else:
                query = params + """ WHERE se.start_date <= %s AND se.end_date >= %s  AND sc.id = %s """
                self.env.cr.execute(query, (to_date, from_date, club_id))
                report = self.env.cr.dictfetchall()
            print(report)
        else:
            if not from_date and to_date:
                query = params  + """ WHERE se.end_date <= %s OR se.start_date <= %s """
                self.env.cr.execute(query, (to_date, to_date,))
                report = self.env.cr.dictfetchall()
            elif not to_date and from_date:
                query = """ WHERE se.start_date >= %s OR se.end_date >= %s  """
                self.env.cr.execute(query, (from_date, from_date,))
                report = self.env.cr.dictfetchall()
            elif not from_date and not to_date:
                query = params
                self.env.cr.execute(query)
                report = self.env.cr.dictfetchall()
            else:
                query = params + """ WHERE se.start_date <= %s AND se.end_date >= %s  """
                self.env.cr.execute(query, (to_date, from_date,))
                report = self.env.cr.dictfetchall()
            print(report)
        print(club_id)
        if not report:
            raise UserError('No record found')

        return {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'data': {
                'model': 'event.information',
                'options': json.dumps({
                            'report': report,
                            'from_date':from_date,
                            'to_date':to_date,
                            'club_id': club_id,
                        }, default=json_default),
                'output_format': 'xlsx',
                'report_name': 'Event Excel Report',
            }
        }

    def get_xlsx_report(self, record, response):
        """Generate xlsx report"""
        print('sdfghjkl')
        report = record['report']
        data = report[0]
        club_id = record['club_id']
        from_date =record['from_date']
        to_date = record['to_date']

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Event Report')

        bold = workbook.add_format({'bold': True})
        center = workbook.add_format({'align': 'center'})
        title = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
        header = workbook.add_format({'bold': True, 'bg_color': '#eeeeee', 'border': 1, 'align': 'center'})

        sheet.set_column(0, 10, 12)
        company = self.env.company
        print(company.name)
        sheet.write('F4', company.name)
        sheet.merge_range('F5:G5', company.street)
        sheet.write('F6', company.country_id.name)
        sheet.write('G6', company.zip)

        sheet.merge_range('A2:G1', 'School Event Report', title)
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        sheet.write('A4', 'Date:', bold)
        sheet.write('B4', date_str,center)
        if from_date and to_date:
            sheet.write('A5', 'From', bold)
            sheet.write('B5', f'{from_date}', center)
            sheet.write('C5', 'To', bold)
            sheet.write('D5', f'{to_date}', center)
        elif from_date and not to_date:
            sheet.write('A5', 'From', bold)
            sheet.write('B5', f'{from_date}', center)
        elif to_date and not from_date:
            sheet.write('A5', 'To', bold)
            sheet.write('B5', f'{to_date}', center)


        if club_id :
            sheet.write('A7', 'Club :', bold)
            sheet.write('B7', data.get('cname'),center)
            sheet.write('A8', 'Incharge :', bold)
            sheet.write('B8', data.get('rname'),center)

            headers = ['Sl.No', 'Event Name', 'From Date', 'To Date', 'Status']

            for col, h in enumerate(headers):
                sheet.write(9, col, h, header)

            index = 1
            row = 10
            for record in report:
                sheet.write(row, 0, index,center)
                sheet.write(row, 1, record['name'],center)
                sheet.write(row, 2, record['start_date'],center)
                sheet.write(row, 3, record['end_date'],center)
                sheet.write(row, 4, record['status'],center)

                row += 1
                index += 1
        else:
            headers = ['Sl.No', 'Event Name', 'From Date', 'To Date', 'Status','Club', 'Incharge']

            for col, h in enumerate(headers):
                sheet.write(7, col, h, header)

            index = 1
            row = 8
            for record in report:
                sheet.write(row, 0, index,center)
                sheet.write(row, 1, record['name'],center)
                sheet.write(row, 2, record['start_date'],center)
                sheet.write(row, 3, record['end_date'],center)
                sheet.write(row, 4, record['status'],center)
                sheet.write(row, 5, record['cname'],center)
                sheet.write(row, 6, record['rname'],center)

                row += 1
                index += 1


        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()


    @api.onchange('period')
    def _onchange_period(self):
        """To calculate the from and to date according to the period"""
        today = fields.Date.today()
        if self.period == 'day':
            self.from_date = today
            self.to_date = today
        elif self.period == 'week':
            first_day = date_utils.start_of(today, 'week')
            last_day = date_utils.end_of(today, 'week')
            self.from_date = first_day
            self.to_date = last_day
        elif self.period == 'month':
            first_day = date_utils.start_of(today, 'month')
            last_day = date_utils.end_of(today, 'month')
            self.from_date = first_day
            self.to_date = last_day


