# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import UserError


class EventInformationReport(models.AbstractModel):
    """Receiving the event information nad prepare data on the server side for report"""
    _name = 'report.school_management.event_information_report'
    _description = 'Event Report'

    def _get_report_values(self, docids, data=None):
        """Passing the club data to template"""

        from_date = data.get('from_date')
        to_date = data.get('to_date')
        club_id = data.get('club_id')


        if from_date and to_date:
            if from_date > to_date:
                raise UserError('Invalid date range')

        if club_id:
            if not from_date and to_date:
                query = """
                             SELECT 
                                    se.name,se.start_date, se.end_date,se.status,
                                      sc.name as cname, rp.name as rname
                                FROM school_events se
                                JOIN school_club sc ON se.club_id = sc.id
                                JOIN res_partner rp ON sc.incharge_id = rp.id
                                WHERE (se.start_date <= %s OR se.end_date <= %s)  AND sc.id = %s
                            """
                self.env.cr.execute(query, (to_date, to_date, club_id))
                report = self.env.cr.dictfetchall()
            elif not to_date and from_date:
                query = """
                         SELECT 
                                se.name,se.start_date, se.end_date,se.status,
                                  sc.name as cname, rp.name as rname
                            FROM school_events se
                            JOIN school_club sc ON se.club_id = sc.id
                            JOIN res_partner rp ON sc.incharge_id = rp.id
                            WHERE (se.start_date >= %s OR se.end_date >= %s)  AND sc.id = %s
                        """
                self.env.cr.execute(query, (from_date, from_date, club_id))
                report = self.env.cr.dictfetchall()
            elif not to_date and not from_date:
                query = """
                         SELECT 
                                se.name,se.start_date, se.end_date,se.status,
                                  sc.name as cname, rp.name as rname
                            FROM school_events se
                            JOIN school_club sc ON se.club_id = sc.id
                            JOIN res_partner rp ON sc.incharge_id = rp.id
                        """
                self.env.cr.execute(query)
                report = self.env.cr.dictfetchall()
            else:
                query = """
                         SELECT 
                                se.name,se.start_date, se.end_date,se.status,
                                  sc.name as cname, rp.name as rname
                            FROM school_events se
                            JOIN school_club sc ON se.club_id = sc.id
                            JOIN res_partner rp ON sc.incharge_id = rp.id
                            WHERE se.start_date <= %s AND se.end_date >= %s  AND sc.id = %s
                        """
                self.env.cr.execute(query, (to_date,from_date,club_id))
                report = self.env.cr.dictfetchall()
            print(report)
        else:
            if not from_date and to_date:
                query = """
                                SELECT 
                                    se.name,se.start_date, se.end_date,se.status,
                                      sc.name as cname, rp.name as rname
                                FROM school_events se
                                JOIN school_club sc ON se.club_id = sc.id
                                JOIN res_partner rp ON sc.incharge_id = rp.id
                                WHERE se.end_date <= %s OR se.start_date <= %s    
                        """
                self.env.cr.execute(query, (to_date, to_date,))
                report = self.env.cr.dictfetchall()
            elif not to_date and from_date:
                query = """
                                SELECT 
                                    se.name,se.start_date, se.end_date,se.status,
                                      sc.name as cname, rp.name as rname
                                FROM school_events se
                                JOIN school_club sc ON se.club_id = sc.id
                                JOIN res_partner rp ON sc.incharge_id = rp.id
                                WHERE se.start_date >= %s OR se.end_date >= %s  
                        """
                self.env.cr.execute(query, (from_date, from_date,))
                report = self.env.cr.dictfetchall()
            elif not from_date and not to_date:
                query = """
                                SELECT 
                                    se.name,se.start_date, se.end_date,se.status,
                                      sc.name as cname, rp.name as rname
                                FROM school_events se
                                JOIN school_club sc ON se.club_id = sc.id
                                JOIN res_partner rp ON sc.incharge_id = rp.id
                        """
                self.env.cr.execute(query)
                report = self.env.cr.dictfetchall()
            else:
                query = """
                                SELECT 
                                    se.name,se.start_date, se.end_date,se.status,
                                      sc.name as cname, rp.name as rname
                                FROM school_events se
                                JOIN school_club sc ON se.club_id = sc.id
                                JOIN res_partner rp ON sc.incharge_id = rp.id
                                WHERE se.start_date <= %s AND se.end_date >= %s  
                        """
                self.env.cr.execute(query, (to_date,from_date,))
                report = self.env.cr.dictfetchall()
            print(report)
        if not report:
            raise UserError('No record found')
        return {
            'docs': report,
            'club_id': club_id,
            'from_date': from_date,
            'to_date': to_date,
            'data': data,
        }
