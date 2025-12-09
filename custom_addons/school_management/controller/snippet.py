from odoo import http
from odoo.http import request

class WebsiteProduct(http.Controller):
    @http.route('/get_event_details', auth="public", type='jsonrpc', website=True)
    def get_event_details(self):
        """Get the website events for the snippet."""
        events = request.env[
            'school.events'].sudo().search_read([('image', '!=', False)],
                    fields=['name', 'image', 'id', 'start_date', 'end_date', 'name','club_id'])
        values = {
            'events': events,
        }
        return values

    @http.route('/event_details/<int:id>', auth="public", type='http', website=True)
    def event_details(self, id=None):
        """Get the website event details."""
        event = request.env['school.events'].browse(int(id))
        print(event)
        return request.render('school_management.event_details_template', {
            'event': event,
        })


