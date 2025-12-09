# -*- coding: utf-8 -*-
import base64
import datetime
import io
import json

import xlsxwriter
from odoo import fields,models
from odoo.exceptions import UserError
from odoo.tools import json_default


class LeaveInformation(models.TransientModel):
    """Create the wizard for club report"""
    _name = 'club.information'
    _description = 'Club Information'

    club_id = fields.Many2one('school.club')
    student_id = fields.Many2one('student.registration')

    def action_print_report(self):
        """Returns from ir.actions.report action for creating pdf report"""

        student_id = self.student_id.id if self.student_id else None
        club_id = self.club_id.id if self.club_id else None

        return self.env.ref('school_management.action_club_information_report').report_action(
            None,
            data={
                'student_id': student_id,
                'club_id' : club_id
            }
        )

    def action_xl_report(self):
        """Returns from ir.actions.report action for creating xlsx report"""
        student_id = self.student_id.id if self.student_id else 0
        club_id = self.club_id.id if self.club_id else 0
        params = """
                SELECT 
                        s.admission_no, s.first_name, s.last_name, s.email, s.gender, 
                        sc.name as cname,
                        c.name as class, 
                        rp.name as rname
                    FROM student_registration s
                    JOIN school_club_student_registration_rel rel ON s.id = rel.student_registration_id
                    JOIN school_club sc ON rel.school_club_id = sc.id
                    JOIN res_partner rp ON sc.incharge_id = rp.id
                    JOIN student_class c ON s.current_class_id = c.id
        """


        if not club_id and not student_id:
            clubs = self.env['school.club'].search([]).mapped('name')
        else:
            clubs = self.env['school.club'].search([('id', '=', club_id)])
        if student_id:
            query = params +  """WHERE s.id = %s """
            self.env.cr.execute(query, (student_id,))
            report = self.env.cr.dictfetchall()
        elif club_id and not student_id:
            query = params + """ WHERE  sc.id = %s """
            self.env.cr.execute(query, (club_id,))
            report = self.env.cr.dictfetchall()
        else:
            query = params
            self.env.cr.execute(query)
            report = self.env.cr.dictfetchall()
        if not report:
            raise UserError('No record found')

        return {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
             'data':{
                 'model': 'club.information',
                 'options' : json.dumps({
                            'report': report,
                            'student_id': student_id,
                            'club_id': club_id,
                        }, default=json_default),
                 'output_format': 'xlsx',
                 'report_name': 'Club Excel Report',
            }
        }

    def get_xlsx_report(self, record, response):
        """Generate xlsx report"""

        report = record['report']
        data = report[0]
        student_id = record['student_id']
        club_id = record['club_id']

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Club Report')

        bold = workbook.add_format({'bold': True})
        center = workbook.add_format({'align': 'center'})
        title = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
        header = workbook.add_format({'bold': True, 'bg_color': '#eeeeee', 'border': 1, 'align': 'center'})


        sheet.set_column(0, 10, 12)
        company = self.env.company
        sheet.write('H4',company.name)
        sheet.merge_range('H5:I5',company.street)
        sheet.write('H6',company.country_id.name)
        sheet.write('I6',company.zip)

        sheet.merge_range('A2:I1', 'School Club Report', title)
        date_str =  datetime.datetime.now().strftime('%Y-%m-%d')
        sheet.write('A4', 'Date:', bold)
        sheet.write('B4', date_str,center)

        if student_id :
            print('inn')
            sheet.write('A6', 'Admission No:', bold)
            sheet.write('B6', data.get('admission_no'),center)
            sheet.write('A7', 'Name:', bold)
            sheet.write('B7', f"{data['first_name']} {data['last_name']}",center)
            sheet.write('A8', 'Class:', bold)
            sheet.write('B8', data['class'],center)

            headers = ['Email', 'Gender', 'Club ', 'Incharge']

            for col, h in enumerate(headers):
                sheet.write(9, col, h, header)

            row = 10
            data = report[0]
            p = dict(self.env['student.registration']._fields['gender'].selection).get(data['gender'])
            sheet.write(row, 0, data['email'],center)
            sheet.write(row, 1, p,center)
            sheet.write(row, 2, data['cname'],center)
            sheet.write(row, 3, data['rname'],center)

        elif club_id  and not student_id :

            sheet.write('A6', 'Club :', bold)
            sheet.write('B6', data.get('cname'),center)
            sheet.write('A7', 'Incharge :', bold)
            sheet.write('B7', data.get('rname'),center)

            headers = ['Sl.No','Admission No','First Name','Last Name','Class','Email', 'Gender']

            for col, h in enumerate(headers):
                sheet.write(8, col, h, header)

            row = 9
            index = 1
            for record in report:
                p = dict(self.env['student.registration']._fields['gender'].selection).get(record['gender'])
                sheet.write(row, 0, index,center)
                sheet.write(row, 1, record['admission_no'],center)
                sheet.write(row, 2, record['first_name'],center)
                sheet.write(row, 3, record['last_name'],center)
                sheet.write(row, 4, record['class'],center)
                sheet.write(row, 5, record['email'],center)
                sheet.write(row, 6, p,center)
                row += 1
                index += 1

        else:
            clubs = []
            for r in report:
                if r.get('cname') not in clubs:
                    clubs.append(r.get('cname'))
            row = 6
            headers = ['Sl.No','Admission No','First Name','Last Name','Class','Email', 'Gender','Club','Incharge']
            for club in clubs:
                row += 2
                index = 1
                sheet.merge_range(f'A{row}:I{row}', f"{club}" , title )
                row += 1
                for col, h in enumerate(headers):
                    sheet.write(row, col, h, header)
                row += 1
                for record in report:
                    if record['cname'] == club:
                        p = dict(self.env['student.registration']._fields['gender'].selection).get(record['gender'])
                        sheet.write(row, 0, index,center)
                        sheet.write(row, 1, record['admission_no'],center)
                        sheet.write(row, 2, record['first_name'],center)
                        sheet.write(row, 3, record['last_name'],center)
                        sheet.write(row, 4, record['class'],center)
                        sheet.write(row, 5, record['email'],center)
                        sheet.write(row, 6, p,center)
                        sheet.write(row, 7, record['cname'],center)
                        sheet.write(row, 8, record['rname'],center)
                        row += 1
                        index += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()


