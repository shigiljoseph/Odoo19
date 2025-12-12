# -*- coding: utf-8 -*-
import base64

from odoo import http
from odoo.http import request


class WebFormController(http.Controller):
    @http.route('/school_events', auth='public', website=True)
    def display_web_form(self, **kwargs):
        print('innn')
        clubs = self.env['school.club'].search([])
        return request.render('school_management.school_event_form_template', {
            'clubs': clubs,
        })

    @http.route('/submit/event', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def handle_web_form_submission(self, **post):
        """Create the student leave record"""
        print("inn")
        image_data = post.get('image')
        if image_data:
            image_binary = base64.b64encode(image_data.read())
        else:
            image_binary = False
        request.env['school.events'].sudo().create({
            'name': post.get('name'),
            'club_id': int(post.get('club_id')),
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
            'image' : image_binary
        })
        return request.redirect('/school_events')