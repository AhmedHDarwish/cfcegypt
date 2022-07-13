from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AbstractSalesTarget(models.AbstractModel):
    _inherit = 'abstract.sales.target'

    sale_order_ids = fields.Many2many('sale.order', string='Sales Orders', compute='_compute_sale_order_ids', store=True)

    sale_orders_count = fields.Integer('Sales Orders Count', compute='_compute_sale_orders_count', store=True)

    untaxed_sales_total = fields.Float(string='Untaxed Sales Total', compute='_compute_sales_total', store=True,
                                help="Untaxed Sales Total which is computed by summary of all untaxed sales amount recorded in Sales"
                                " Management application.")
    sales_target_reached = fields.Float(string='Sales Target Reached', compute='_compute_sales_target_reached', store=True,
                                        help="The Sales Target Reached is computed based on the Untaxed Sales Total and the approved Target."
                                        " I.e. Sales Target Reached = 100 * Untaxed Sales Total / Target")

    # compute from invoice data
    sales_invoice_ids = fields.Many2many('account.move', string='Invoices', compute='_compute_sales_invoice_ids', store=True)

    sales_invoices_count = fields.Integer(string='Invoices Count', compute='_compute_sales_invoices_count', store=True)
    sales_invoiced = fields.Float(string='Invoiced Total', compute='_compute_sales_invoiced', store=True)

    invoiced_target_reached = fields.Float(string='Invoiced Target Reached', compute='_compute_invoiced_target_reached', store=True)

    # compute from all channels
    sales_total = fields.Float(string='Sales Total', compute='_compute_all_channel_sales_total', store=True,
                               help="Sales Total from all channels (e.g. Sales, PoS, Website).\n"
                               "Note: Revenue recorded in Sales Management applications will not be included here unless it is invoiced")
    target_reached = fields.Float(string='Target Reached', compute='_compute_target_reached', store=True, help="The Target Reached is computed"
                                  " based on the Sales Total and the approve Target. I.e. Target Reached = 100 * Sales Total / Target")

    def _get_sales_orders(self):
        raise ValidationError(_("The method `_get_sales_orders` has not been implemented for the model '%s'") % self._name)

    def _compute_sale_order_ids(self):
        for r in self:
            if r.state == 'approved':
                sale_order_ids = r._get_sales_orders()
                r.sale_order_ids = sale_order_ids.ids
            else:
                r.sale_order_ids = []

    @api.depends('sale_order_ids')
    def _compute_sale_orders_count(self):
        for r in self:
            r.sale_orders_count = len(r.sale_order_ids)

    def _get_sale_report_domain(self):
        raise ValidationError(_("The method `_get_sale_report_domain` has not been implemented for the model '%s'") % self._name)

    @api.depends('sale_order_ids')
    def _compute_sales_total(self):
        SaleReport = self.env['sale.report'].sudo()
        for r in self:
            domain = r._get_sale_report_domain()
            sales_report_line_ids = SaleReport.search(domain)
            r.untaxed_sales_total = sum(sales_report_line_ids.mapped('price_subtotal'))

    @api.depends('target', 'untaxed_sales_total')
    def _compute_sales_target_reached(self):
        for r in self:
            if r._is_zero_target():
                r.sales_target_reached = 0.0
            else:
                r.sales_target_reached = 100.0 * r.untaxed_sales_total / r.target

    def _get_sales_invoices(self):
        raise ValidationError(_("The method `_get_sales_invoices` has not been implemented for the model '%s'") % self._name)

    def _compute_sales_invoice_ids(self):
        for r in self:
            if r.state == 'approved':
                sales_invoice_ids = r._get_sales_invoices()
                r.sales_invoice_ids = sales_invoice_ids.ids
            else:
                r.sales_invoice_ids = []

    @api.depends('sales_invoice_ids')
    def _compute_sales_invoices_count(self):
        for r in self:
            r.sales_invoices_count = len(r.sales_invoice_ids)

    def _get_sales_invoices_domain(self):
        raise ValidationError(_("The method `_get_sales_invoices_domain` has not been implemented for the model '%s'") % self._name)

    @api.depends('sales_invoice_ids')
    def _compute_sales_invoiced(self):
        InvoiceReport = self.env['account.invoice.report'].sudo()
        for r in self:
            domain = r._get_sales_invoices_domain()
            sales_invoiced_report_line_ids = InvoiceReport.search(domain)
            r.sales_invoiced = sum(sales_invoiced_report_line_ids.mapped('price_subtotal'))

    @api.depends('target', 'sales_invoiced')
    def _compute_invoiced_target_reached(self):
        for r in self:
            if r._is_zero_target():
                r.invoiced_target_reached = 0.0
            else:
                r.invoiced_target_reached = 100.0 * r.sales_invoiced / r.target

    @api.depends('sales_invoiced')
    def _compute_all_channel_sales_total(self):
        for r in self:
            r.sales_total = r.sales_invoiced

    @api.depends('target', 'sales_total')
    def _compute_target_reached(self):
        for r in self:
            if r._is_zero_target():
                r.target_reached = 0.0
            else:
                r.target_reached = 100.0 * r.sales_total / r.target

    def action_view_sale_orders(self):
        action = self.env.ref('sale.action_orders')
        result = action.read()[0]

        sale_order_ids = self.mapped('sale_order_ids')
        so_count = len(sale_order_ids)
        # choose the view_mode accordingly
        if so_count != 1:
            result['domain'] = "[('id', 'in', " + str(sale_order_ids.ids) + ")]"
        elif so_count == 1:
            res = self.env.ref('sale.view_order_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = sale_order_ids.id
        return result

    def action_view_invoices(self):
        action = self.env.ref('account.action_move_out_invoice_type')
        result = action.read()[0]

        sales_invoice_ids = self.mapped('sales_invoice_ids')
        inv_count = len(sales_invoice_ids)
        # choose the view_mode accordingly
        if inv_count != 1:
            result['domain'] = "[('id', 'in', " + str(sales_invoice_ids.ids) + ")]"
        elif inv_count == 1:
            res = self.env.ref('account.view_move_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = sales_invoice_ids.id
        return result
