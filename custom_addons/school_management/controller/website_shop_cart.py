
from odoo import http
from odoo.http import request

class ClearCart(http.Controller):
    @http.route('/shop/clear_cart', type='http', auth='public', website=True)
    def clear_cart(self, **kw):
        SaleOrder = request.env['sale.order']
        order = SaleOrder.search([('website_id', '=', request.website.id), ('state', '=', 'draft')], limit=1)
        if order:
            order.order_line.unlink()
        return request.redirect('/shop/cart')

        # website = request.env['website'].get_current_website()
        # sale_order = request.env['sale.order'].browse()
        # print(request.cart)
        # print(sale_order.order_line)
        # order = sale_order.sudo().search([
        #     ('website_id', '=', website.id),
        #     ('state', '=', 'draft'),
        #     ('partner_id', '=', request.env.user.partner_id.id),
        # ], limit=1)
        #
        # if sale_order:
        #     sale_order.order_line.unlink()

        # order = request.website.sale_get_order()
        # if order:
        #     order.order_line.unlink()
        # return request.redirect('/shop/cart')