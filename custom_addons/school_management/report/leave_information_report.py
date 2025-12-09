# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import UserError


class LeaveInformationReport(models.AbstractModel):
    """Receiving the leave information nad prepare data on the server side for report"""
    _name = 'report.school_management.leave_information_report'
    _description = 'Student Report'

    def _get_report_values(self, docids, data=None):
        """Passing the club data to template"""

        from_date = data.get('from_date')
        to_date = data.get('to_date')
        student_id = data.get('student_id')
        student_class_id = data.get('student_class_id')


        if from_date and to_date:
            if from_date > to_date:
                raise UserError('Invalid date range')

        if student_id:
            if not from_date and to_date:
                query = """
                            SELECT 
                                 s.admission_no, s.first_name, s.last_name, s.email, s.gender,
                                 sl.start_date, sl.end_date, sl.reason,sl.total_days,
                                 sc.name as cname
                                 FROM student_leave sl
                                 JOIN student_registration s ON sl.student_id = s.id
                                 JOIN student_class sc ON s.current_class_id = sc.id
                                 WHERE  (sl.end_date <= %s OR sl.start_date <= %s)   AND s.id = %s
                        """
                self.env.cr.execute(query, (to_date,to_date, student_id))
                report = self.env.cr.dictfetchall()
                student_class = self.env['school.events'].search([('id', '=', student_class_id)])
                if report[0]['cname'] != student_class.name:
                    raise UserError('No record')
            elif not to_date and from_date:
                query = """
                            SELECT 
                                 s.admission_no, s.first_name, s.last_name, s.email, s.gender,
                                 sl.start_date, sl.end_date, sl.reason,sl.total_days,
                                 sc.name as cname
                                 FROM student_leave sl
                                 JOIN student_registration s ON sl.student_id = s.id
                                 JOIN student_class sc ON s.current_class_id = sc.id
                                 WHERE (sl.start_date >= %s  OR sl.end_date >= %s)  AND s.id = %s
                        """
                self.env.cr.execute(query, (from_date,from_date, student_id))
                report = self.env.cr.dictfetchall()

            elif not from_date and not to_date:
                query = """
                            SELECT 
                                 s.admission_no, s.first_name, s.last_name, s.email, s.gender,
                                 sl.start_date, sl.end_date, sl.reason,sl.total_days,
                                 sc.name as cname
                                 FROM student_leave sl
                                 JOIN student_registration s ON sl.student_id = s.id
                                 JOIN student_class sc ON s.current_class_id = sc.id
                        """
                self.env.cr.execute(query)
                report = self.env.cr.dictfetchall()
            else:
                query = """
                                SELECT 
                                    s.admission_no, s.first_name, s.last_name, s.email, s.gender,
                                    sl.start_date, sl.end_date, sl.reason,sl.total_days,
                                    sc.name as cname
                                FROM student_leave sl
                                JOIN student_registration s ON sl.student_id = s.id
                                JOIN student_class sc ON s.current_class_id = sc.id
                                WHERE sl.start_date <= %s AND sl.end_date >= %s   AND s.id = %s
                            """
                self.env.cr.execute(query, (to_date,from_date,student_id))
                report = self.env.cr.dictfetchall()
        elif student_class_id and not student_id:
            if not from_date and to_date:
                query = """
                            SELECT 
                                s.admission_no, s.first_name, s.last_name, s.email, s.gender,s.current_class_id,
                                sl.start_date, sl.end_date, sl.reason,sl.total_days,
                                sc.name as cname
                            FROM student_leave sl
                            JOIN student_registration s ON sl.student_id = s.id
                            JOIN student_class sc ON s.current_class_id = sc.id
                            WHERE  s.current_class_id = %s AND (sl.end_date <= %s OR sl.start_date<= %s )   
                        """
                self.env.cr.execute(query, (student_class_id,to_date,to_date,))
                report = self.env.cr.dictfetchall()
            elif not to_date and from_date:
                query = """
                            SELECT 
                                s.admission_no, s.first_name, s.last_name, s.email, s.gender,
                                sl.start_date, sl.end_date, sl.reason,sl.total_days,
                                sc.name as cname
                            FROM student_leave sl
                            JOIN student_registration s ON sl.student_id = s.id
                            JOIN student_class sc ON s.current_class_id = sc.id
                            WHERE (sl.start_date >= %s  OR sl.end_date >= %s) AND s.current_class_id = %s   
                        """
                self.env.cr.execute(query, (from_date,from_date, student_class_id))
                report = self.env.cr.dictfetchall()
            elif not from_date and not to_date:
                query = """
                            SELECT 
                                s.admission_no, s.first_name, s.last_name, s.email, s.gender,
                                sl.start_date, sl.end_date, sl.reason,sl.total_days,
                                sc.name as cname
                            FROM student_leave sl
                            JOIN student_registration s ON sl.student_id = s.id
                            JOIN student_class sc ON s.current_class_id = sc.id
                        """
                self.env.cr.execute(query )
                report = self.env.cr.dictfetchall()
            else:
                query = """
                    SELECT 
                        s.admission_no, s.first_name, s.last_name, s.email, s.gender,
                        sl.start_date, sl.end_date, sl.reason,sl.total_days,
                        sc.name as cname
                    FROM student_leave sl
                    JOIN student_registration s ON sl.student_id = s.id
                    JOIN student_class sc ON s.current_class_id = sc.id
                    WHERE sl.start_date <= %s AND sl.end_date >= %s AND s.current_class_id = %s   
                """
                self.env.cr.execute(query, (to_date,from_date, student_class_id))
                report = self.env.cr.dictfetchall()
        else:
            print('hi',from_date,to_date)
            if not from_date and to_date:
                query = """
                            SELECT 
                                s.admission_no, s.first_name, s.last_name, s.email, s.gender,
                                sl.start_date, sl.end_date, sl.reason,sl.total_days,
                                sc.name as cname
                            FROM student_leave sl
                            JOIN student_registration s ON sl.student_id = s.id
                            JOIN student_class sc ON s.current_class_id = sc.id
                            WHERE  sl.end_date <= %s OR sl.start_date <= %s    
                        """
                self.env.cr.execute(query, (to_date,to_date))
                report = self.env.cr.dictfetchall()
            elif not to_date and from_date:
                query = """
                            SELECT 
                                s.admission_no, s.first_name, s.last_name, s.email, s.gender,
                                sl.start_date, sl.end_date, sl.reason,sl.total_days,
                                sc.name as cname
                            FROM student_leave sl
                            JOIN student_registration s ON sl.student_id = s.id
                            JOIN student_class sc ON s.current_class_id = sc.id
                            WHERE sl.start_date >= %s  OR sl.end_date >= %s
                        """
                self.env.cr.execute(query, (from_date,from_date))
                report = self.env.cr.dictfetchall()
            elif( not from_date and not to_date):
                print('hi')
                query = """
                            SELECT 
                                s.admission_no, s.first_name, s.last_name, s.email, s.gender,
                                sl.start_date, sl.end_date, sl.reason,sl.total_days,
                                sc.name as cname
                            FROM student_leave sl
                            JOIN student_registration s ON sl.student_id = s.id
                            JOIN student_class sc ON s.current_class_id = sc.id
                        """
                self.env.cr.execute(query)
                report = self.env.cr.dictfetchall()
            else:
                query = """
                    SELECT 
                        s.admission_no, s.first_name, s.last_name, s.email, s.gender,
                        sl.start_date, sl.end_date, sl.reason,sl.total_days,
                        sc.name as cname
                    FROM student_leave sl
                    JOIN student_registration s ON sl.student_id = s.id
                    JOIN student_class sc ON s.current_class_id = sc.id
                    WHERE sl.start_date <= %s AND sl.end_date >= %s    
                """
                self.env.cr.execute(query, (to_date,from_date,))
                report = self.env.cr.dictfetchall()
            print(report)
        if not report:
            raise UserError('No record Found')
        return {
            'docs': report,
            'from_date': from_date,
            'to_date': to_date,
            'student_id':student_id,
            'student_class_id': student_class_id,
            'data': data,
        }
