# -*- coding: utf-8 -*-

import datetime
import io
import json
import xlsxwriter
from odoo import api,fields,models
from odoo.exceptions import UserError
from odoo.tools import json_default,date_utils


class LeaveInformation(models.TransientModel):
    """Create the wizard for leave report"""
    _name = 'leave.information'
    _description = 'Leave Information'

    period = fields.Selection([('day','Day'),('week','Weekly'),('month','Monthly'),('custom','Custom')],
                              default='custom',required=True)
    student_class_id = fields.Many2one('student.class')
    student_id = fields.Many2one('student.registration')
    from_date = fields.Date()
    to_date = fields.Date()

    def action_print_report(self):
        """Pass data to ir.actions.report action"""

        from_date = self.from_date
        to_date = self.to_date
        student_id = self.student_id.id if self.student_id else None
        student_class_id = self.student_class_id.id if self.student_class_id else None

        return self.env.ref('school_management.action_leave_information_report').report_action(
            None,
            data={
                "from_date": from_date,
                "to_date": to_date,
                "student_id": student_id,
                "student_class_id":student_class_id
            }
        )


    def action_xl_report(self):
        """Returns ir.actions.report action for creating xlsx report"""

        from_date = self.from_date
        to_date = self.to_date
        student_id = self.student_id.id
        student_class_id = self.student_class_id.id

        if from_date and to_date:
            if from_date > to_date:
                raise UserError('Invalid date range')

        params = """SELECT 
                         s.admission_no, s.first_name, s.last_name, s.email, s.gender,
                         sl.start_date, sl.end_date, sl.reason,sl.total_days,
                         sc.name as cname
                         FROM student_leave sl
                         JOIN student_registration s ON sl.student_id = s.id
                         JOIN student_class sc ON s.current_class_id = sc.id
                """

        if student_id:
            if not from_date and to_date:
                query = params +  """ WHERE  (sl.end_date <= %s OR sl.start_date <= %s)   AND s.id = %s  """
                self.env.cr.execute(query, (to_date, to_date, student_id))
                report = self.env.cr.dictfetchall()
            elif not to_date and from_date:
                query = params + """WHERE (sl.start_date >= %s  OR sl.end_date >= %s)  AND s.id = %s  """
                self.env.cr.execute(query, (from_date, from_date, student_id))
                report = self.env.cr.dictfetchall()

            elif not from_date and not to_date:
                query = params
                self.env.cr.execute(query)
                report = self.env.cr.dictfetchall()
            else:
                query = params + """ WHERE sl.start_date <= %s AND sl.end_date >= %s   AND s.id = %s """
                self.env.cr.execute(query, (to_date, from_date, student_id))
                report = self.env.cr.dictfetchall()
        elif student_class_id and not student_id:
            if not from_date and to_date:
                query = params + """WHERE  s.current_class_id = %s AND (sl.end_date <= %s OR sl.start_date<= %s )  """
                self.env.cr.execute(query, (student_class_id, to_date, to_date,))
                report = self.env.cr.dictfetchall()
            elif not to_date and from_date:
                query = params + """WHERE (sl.start_date >= %s  OR sl.end_date >= %s) AND s.current_class_id = %s """
                self.env.cr.execute(query, (from_date, from_date, student_class_id))
                report = self.env.cr.dictfetchall()
            elif not from_date and not to_date:
                query = params
                self.env.cr.execute(query)
                report = self.env.cr.dictfetchall()
            else:
                query = params + """WHERE sl.start_date <= %s AND sl.end_date >= %s AND s.current_class_id = %s  """
                self.env.cr.execute(query, (to_date, from_date, student_class_id))
                report = self.env.cr.dictfetchall()
        else:
            if not from_date and to_date:
                query = params + """WHERE  sl.end_date <= %s OR sl.start_date <= %s """
                self.env.cr.execute(query, (to_date, to_date))
                report = self.env.cr.dictfetchall()
            elif not to_date and from_date:
                query = params + """WHERE sl.start_date >= %s  OR sl.end_date >= %s"""
                self.env.cr.execute(query, (from_date, from_date))
                report = self.env.cr.dictfetchall()
            elif (not from_date and not to_date):
                query = params
                self.env.cr.execute(query)
                report = self.env.cr.dictfetchall()
            else:
                query = params + """WHERE sl.start_date <= %s AND sl.end_date >= %s"""
                self.env.cr.execute(query, (to_date, from_date,))
                report = self.env.cr.dictfetchall()
            print(report)

        if not report:
            raise UserError('No record found')

        return {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'data': {
                'model': 'leave.information',
                'options': json.dumps({
                            'report': report,
                            'from_date':from_date,
                            'to_date':to_date,
                            'student_id':student_id,
                            'student_class_id':student_class_id,
                        }, default=json_default),
                'output_format': 'xlsx',
                'report_name': 'Leave Excel Report',
            }
        }

    def get_xlsx_report(self, record, response):
        """Generate xlsx report"""

        report = record['report']
        data = report[0]
        student_id = record['student_id']
        student_class_id = record['student_class_id']
        from_date = record['from_date']
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
        sheet.write('H4', company.name)
        sheet.merge_range('H5:I5', company.street)
        sheet.write('H6', company.country_id.name)
        sheet.write('I6', company.zip)

        sheet.merge_range('A2:K1', 'School Leave Report', title)
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        sheet.write('A4', 'Date:', bold)
        sheet.write('B4', date_str, center)
        if from_date and to_date:
            sheet.write('A5', 'From', bold)
            sheet.write('B5', f'{from_date}', bold)
            sheet.write('C5', 'To', bold)
            sheet.write('D5', f'{to_date}', bold)
        elif from_date and not to_date:
            sheet.write('A5', 'From', bold)
            sheet.write('B5', f'{from_date}', bold)
        elif to_date and not from_date:
            sheet.write('A5', 'To', bold)
            sheet.write('B5', f'{to_date}', bold)

        if student_id:
            sheet.write('A7', 'Admission No :', bold)
            sheet.write('B7', data.get('admission_no'),center)
            sheet.write('A8', 'Name :', bold)
            sheet.write('B8', data.get('first_name'),center)
            sheet.write('C8', data.get('last_name'),center)
            sheet.write('A9', 'Class :', bold)
            sheet.write('B9', data.get('cname'),center)



            headers = [ 'Class','Email','Gender', 'From Date', 'To Date', 'Duration','Reason']

            for col, h in enumerate(headers):
                sheet.write(10, col, h, header)

            p = dict(self.env['student.registration']._fields['gender'].selection).get(data['gender'])
            sheet.write(11,0,data['cname'],center)
            sheet.write(11,1,data['email'],center)
            sheet.write(11,2,p,center)
            sheet.write(11,3,data['start_date'],center)
            sheet.write(11,4,data['end_date'],center)
            sheet.write(11,5,data['total_days'],center)
            sheet.write(11,6,data['reason'],center  )

        elif student_class_id and not student_id:

            sheet.write('A7', 'Class :', bold)
            sheet.write('B7', data.get('cname'),center)

            headers = ['Sl.No','Admission No','First Name','Last Name','Email','Gender', 'From Date', 'To Date',
                       'Duration','Reason']

            for col, h in enumerate(headers):
                sheet.write(8, col, h, header)
            row = 9
            index = 1

            for record in report:
                p = dict(self.env['student.registration']._fields['gender'].selection).get(record['gender'])
                sheet.write(row,0,index, center)
                sheet.write(row, 1, record['admission_no'],center)
                sheet.write(row, 2, record['start_date'],center)
                sheet.write(row, 3, record['end_date'],center)
                sheet.write(row, 4, record['email'],center)
                sheet.write(row, 5, p,center)
                sheet.write(row, 6, record['start_date'],center)
                sheet.write(row, 7, record['end_date'],center)
                sheet.write(row, 8, record['total_days'],center)
                sheet.write(row, 9, record['reason'],center)
                row += 1
                index += 1
        else:
            headers = ['Sl.No', 'Admission No', 'First Name', 'Last Name', 'Class', 'Email', 'Gender', 'From Date', 'To Date',
                       'Duration', 'Reason']

            for col, h in enumerate(headers):
                sheet.write(7, col, h, header)
            row = 8
            index = 1

            for record in report:
                p = dict(self.env['student.registration']._fields['gender'].selection).get(record['gender'])
                sheet.write(row, 0, index,center)
                sheet.write(row, 1, record['admission_no'],center)
                sheet.write(row, 2, record['start_date'],center)
                sheet.write(row, 3, record['end_date'],center)
                sheet.write(row, 4, record['cname'],center)
                sheet.write(row, 5, record['email'],center)
                sheet.write(row, 6, p,center)
                sheet.write(row, 7, record['start_date'],center)
                sheet.write(row, 8, record['end_date'],center)
                sheet.write(row, 9, record['total_days'],center)
                sheet.write(row, 10, record['reason'],center)
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



