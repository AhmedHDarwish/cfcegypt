from odoo import models, fields, api
from odoo.tools import float_is_zero, float_compare


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    st_sales_order_ids = fields.One2many('sale.order', 'team_id', string='Sales Orders',
                                            domain=[('state', 'in', ('sale', 'done'))],
                                             help="Sales Orders whose corresponding Sales Orders are in the states of Sales Order and Locked")

    st_sales_invoice_ids = fields.One2many('account.move', 'team_id', string='Invoices',
                                             domain=[('state', '=', 'posted'), ('type', 'in', ('out_invoice', 'out_refund'))],
                                             help="Customer Invoices that are either in Open or in Paid state")

    invoiced_target = fields.Float(digits='Product Price',
                                   help="Target of invoice revenue for the current month. This is the amount the sales "
                                   "team estimates to be able to invoice this month."
                                   " You can also go to Sales Target Application to define multiple target for the team over the time."
                                   " If a target is defined there for the team, this field becomes readonly.")

    @api.model
    def cron_update_current_month_target(self):
        prec = self.env['decimal.precision'].precision_get('Product Price')
        teams = self.env['crm.team'].search([('approved_targets_count', '>', 0)])
        for r in teams:
            today = fields.Date.today()
            current_month_target, team_sales_target_ids = r.get_month_target(today.month, today.year)

            update_data = {}
            if float_compare(current_month_target, r.invoiced_target, precision_digits=prec) != 0:
                update_data['invoiced_target'] = current_month_target

            if bool(update_data):
                r.write(update_data)
