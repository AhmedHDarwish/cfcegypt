from odoo import fields, models, api
from odoo.tools import float_compare


class ResUsers(models.Model):
    _inherit = 'res.users'

    st_sales_order_ids = fields.One2many('sale.order', 'user_id', string='Sales Orders',
                                            domain=[('state', 'in', ('sale', 'done'))],
                                             help="Sales Orders in the states of Sales Order and Locked")

    st_sales_invoice_ids = fields.One2many('account.move', 'invoice_user_id', string='Invoices',
                                             domain=[('state', '=', 'posted'), ('type', 'in', ('out_invoice', 'out_refund'))],
                                             help="Customer Invoices that are either in Open or in Paid state")

    target_sales_invoiced = fields.Float(digits='Product Price')

    @api.model
    def cron_update_current_month_target(self):
        prec = self.env['decimal.precision'].precision_get('Product Price')
        users = self.env['res.users'].search([('approved_targets_count', '>', 0)])
        date = fields.Date.today()
        for r in users:
            target_sales_invoiced, matched_target_ids = r.get_month_target(date.month, date.year)
            update_data = {}
            if float_compare(target_sales_invoiced, r.target_sales_invoiced, precision_digits=prec) != 0:
                update_data['target_sales_invoiced'] = target_sales_invoiced
            if bool(update_data):
                r.write(update_data)