# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import UserError


class ClubInformationReport(models.AbstractModel):
    """Receiving the club information nad prepare data on the server side for report"""
    _name = 'report.school_management.club_information_report'
    _description = 'Club Report'

    def _get_report_values(self, docids, data=None):
        """Passing the club data to template"""

        student_id = data.get('student_id')
        club_id = data.get('club_id')

        if not club_id and not student_id:
            clubs = self.env['school.club'].search([]).mapped('name')
            print(clubs)
        else:
            clubs =  self.env['school.club'].search([('id' , '=' , club_id)])
        if student_id:
            query = """
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
                            WHERE s.id = %s   
                        """
            self.env.cr.execute(query, (student_id,))
            report = self.env.cr.dictfetchall()
            print(report)
        elif club_id and not student_id:
            query = """
                        SELECT 
                                s.admission_no, s.first_name, s.last_name, s.email, s.gender,
                                c.name as class,                         
                                sc.name as cname, rp.name as rname
                            FROM student_registration s
                            JOIN school_club_student_registration_rel rel ON s.id = rel.student_registration_id
                            JOIN school_club sc ON rel.school_club_id = sc.id
                            JOIN res_partner rp ON sc.incharge_id = rp.id
                            JOIN student_class c ON s.current_class_id = c.id
                            WHERE  sc.id = %s 
            """
            self.env.cr.execute(query, (club_id,))
            report = self.env.cr.dictfetchall()
            print(report)
        else:
            query = """
                         SELECT 
                                s.admission_no, s.first_name, s.last_name, s.email, s.gender,
                                c.name as class, 
                                sc.name as cname, rp.name as rname
                            FROM student_registration s
                            JOIN school_club_student_registration_rel rel ON s.id = rel.student_registration_id
                            JOIN school_club sc ON rel.school_club_id = sc.id
                            JOIN res_partner rp ON sc.incharge_id = rp.id 
                            JOIN student_class c ON s.current_class_id = c.id
            """
            self.env.cr.execute(query)
            report = self.env.cr.dictfetchall()
            print(report)
            print(clubs)
        if not report:
            raise UserError('No record found')
        return {
            'docs': report,
            'club_id': club_id,
            'student_id':student_id,
            'clubs': clubs,
            'data': data,
        }