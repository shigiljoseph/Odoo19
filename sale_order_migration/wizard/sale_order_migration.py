# -*- coding: utf-8 -*-

from odoo import api,fields,models
import xmlrpc.client
from odoo.exceptions import UserError


class BuyProduct(models.TransientModel):
    """Create wizard to migrate sale order"""

    _name = 'sale.order.migration'
    _description = 'sale order migration'

    db19 = fields.Char(string='DB name')

    url19 = fields.Char(string='DB URL', compute='_compute_db_url', readonly=True, store=True)
    user19 = fields.Many2one('res.users',required=True,readonly=True,string='User',
                           default=lambda self: self.env.user)
    password19 = fields.Char(required=True,string='Password')

    db18 = fields.Char(string='DB name')
    url18 = fields.Char(string='DB URL')
    user18 = fields.Many2one('res.users', required=True,string='User')
    password18 = fields.Char(required=True,string='Password')


    def _compute_db_url(self):
        for rec in self:
            if self.env['ir.config_parameter'].sudo().get_param('web.base.url'):
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                rec.url19 = str(base_url)
            else:
                rec.url19 = "URL not available"


    def action_migrate(self):
        """To transfer sale order data from Odoo 18 to 19"""

        # Odoo 18 (source)
        URL_18 = 'http://localhost:8018'
        DB_18 = self.db18
        USER_18 = self.user18.login
        PASS_18 = self.password18
        print('DB_19', self.db19)

        # Connect to Odoo 18
        common_18 = xmlrpc.client.ServerProxy(f'{URL_18}/xmlrpc/2/common')
        uid_18 = common_18.authenticate(DB_18, USER_18, PASS_18, {})
        if not uid_18:
            raise UserError('Invalid Credentials')
        models_18 = xmlrpc.client.ServerProxy(f'{URL_18}/xmlrpc/2/object')

        # Odoo 19 (target)
        URL_19 = 'http://localhost:8019'
        DB_19 = self.db19
        USER_19 = self.user19.login
        PASS_19 = self.password19

        print('username',self.user19.login)
        print('pass',self.password19)

        # Connect to Odoo 19
        common_19 = xmlrpc.client.ServerProxy(f'{URL_19}/xmlrpc/2/common')
        uid_19 = common_19.authenticate(DB_19, USER_19, PASS_19, {})
        if not uid_19:
            raise UserError('Invalid Credentials')
        print('dfghjk')
        models_19 = xmlrpc.client.ServerProxy(f'{URL_19}/xmlrpc/2/object')


        # Fetch all sales orders with full field data
        sale_ids = models_18.execute_kw(DB_18, uid_18, PASS_18, 'sale.order', 'search', [[]])
        sales = models_18.execute_kw(
            DB_18, uid_18, PASS_18,
            'sale.order', 'read', [sale_ids],
        )



        for order in sales:
            partner_name = order['partner_id'][1]
            print('partner_name', partner_name)
            partner_id = self.env['res.partner'].filtered(lambda x:x.name == partner_name)
            if not partner_id:
                partner_id = models_19.execute_kw(DB_19, uid_19, PASS_19,
                                                  'res.partner', 'create', [{'name':partner_name}])
            else:
                partner_id = partner_id[0]

            new_lines = []
            for line_id in order['order_line']:
                line_data = models_18.execute_kw(
                    DB_18, uid_18, PASS_18,
                    'sale.order.line', 'read', [line_id],
                    {'fields': ['product_id', 'name', 'product_uom_qty', 'price_unit']}
                )
                if not line_data:
                    continue
                line_data = line_data[0]
                print('line_data',line_data)

                product_id = line_data['product_id'][0]
                product_ids = self.env['product.product'].browse( product_id)
                print('product_ids',product_ids)

                if product_ids:
                    new_lines.append([{
                        'product_id': product_ids.id,
                        'name': line_data['name'],
                        'product_uom_qty': line_data['product_uom_qty'],
                        'price_unit': line_data['price_unit'],
                    }])

            new_order = {
                'partner_id': partner_id,
                'date_order': order['date_order'],
                'company_id': order['company_id'][0],
                'user_id': order['user_id'][0],
                'team_id': order['team_id'][0],
                'sale_order_template_id': order['sale_order_template_id'][0] if isinstance(
                    order['sale_order_template_id'], (list, tuple)) else order['sale_order_template_id'],
                'currency_id': order['currency_id'][0],
                'order_line': new_lines,
                'amount_untaxed': order['amount_untaxed'],
                'amount_tax': order['amount_tax'],
                'amount_total': order['amount_total'],
                'state': order['state']
            }

            try:
                new_id = models_19.execute_kw(DB_19, uid_19, PASS_19, 'sale.order', 'create', [new_order])
                print(f"Created SO: {order['name']} as ID {new_id}")
            except Exception as e:
                print(f"Failed {order['name']}: {str(e)}")

