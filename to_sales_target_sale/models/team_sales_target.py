from odoo import models, api
from datetime import datetime


class TeamSalesTarget(models.Model):
    _inherit = 'team.sales.target'

    def _get_sales_orders(self):
        start_date = datetime.combine(self.start_date, datetime.min.time())
        end_date = datetime.combine(self.end_date, datetime.max.time())
        return self.crm_team_id.st_sales_order_ids.filtered(lambda o: o.date_order >= start_date \
                                                         and o.date_order <= end_date)

    @api.depends('crm_team_id.st_sales_order_ids', 'crm_team_id.st_sales_order_ids.state', 'state')
    def _compute_sale_order_ids(self):
        super(TeamSalesTarget, self)._compute_sale_order_ids()

    def _get_sale_report_domain(self):
        return [
            ('order_id', 'in', self.sale_order_ids.ids),
            ('team_id', '=', self.crm_team_id.id),
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date),
            ('state', 'in', ('sale', 'done'))
            ]

    def _get_sales_invoices(self):
        return self.crm_team_id.st_sales_invoice_ids.filtered(lambda inv: inv.invoice_date >= self.start_date and inv.invoice_date <= self.end_date)

    @api.depends('crm_team_id.st_sales_invoice_ids', 'crm_team_id.st_sales_invoice_ids.state', 'state')
    def _compute_sales_invoice_ids(self):
        super(TeamSalesTarget, self)._compute_sales_invoice_ids()

    def _get_sales_invoices_domain(self):
        return [
            ('move_id', 'in', self.sales_invoice_ids.ids),
            ('team_id', '=', self.crm_team_id.id),
            ('invoice_date', '>=', self.start_date),
            ('invoice_date', '<=', self.end_date),
            ('type', 'in', ('out_invoice', 'out_refund')),
            ('state', '=', 'posted')]

