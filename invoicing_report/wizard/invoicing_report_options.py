from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class Invocing(models.TransientModel):
    _name = 'invocing.report.options'
    
    sales_team_ids = fields.Many2many(comodel_name="crm.team", string="Sales Team", required=False, )
    sales_person_ids = fields.Many2many('res.users')
    customer_ids = fields.Many2many('res.partner')
    company_ids = fields.Many2many('res.company')
    product_category_ids = fields.Many2many('product.category')
    date_from = fields.Date()
    date_to = fields.Date()
    
    
    def get_domain(self):
        company_ids = [c.id for c in self.env['res.company'].search([])]
        domain = [('move_id.move_type','in',['out_invoice', 'out_refund', 'out_receipt']),('move_id.state','=','posted'),('product_id','!=',False),('quantity','>',0),('company_id','in',company_ids)]
        if self.sales_team_ids:
            domain.append(('move_id.team_id','in',self.sales_team_ids.ids))
            domain.append(('move_id.partner_id.team_id','in',self.sales_team_ids.ids + [False]))
            domain.append('|')
            domain.append(('product_id.categ_id.sales_team_ids','in',self.sales_team_ids.ids))
            domain.append(('product_id.categ_id.sales_team_ids','=',False))
        if self.sales_person_ids:
            domain.append(('move_id.invoice_user_id','in',self.sales_person_ids.ids))
            domain.append(('move_id.partner_id.user_id','in',self.sales_person_ids.ids +  [False]))
            domain.append('|')
            domain.append(('product_id.categ_id.sales_team_ids','in',self.sales_team_ids.ids))
            domain.append(('product_id.categ_id.sales_team_ids','=',False))
        if self.customer_ids:
            domain.append(('move_id.partner_id','in',self.customer_ids.ids))
        if self.product_category_ids:
            domain.append(('product_id.categ_id','in',self.product_category_ids.ids))
        if self.company_ids:
            domain.append(('company_id','in',self.company_ids.ids))
        if self.date_from and self.date_to:
            domain.extend([('move_id.invoice_date','>=',self.date_from),('move_id.invoice_date','<=',self.date_to)])
        return domain
    
    def get_lines(self):
        lines = self.env['account.move.line'].sudo().search(self.get_domain())
        filtered_ids = [line.id for line in lines if len(line.sale_line_ids) > 0]
        lines = self.env['account.move.line'].sudo().search([('id','in',filtered_ids)])
        return lines.sorted(key=lambda r: (r.move_id.team_id.id,r.move_id.invoice_user_id.id,r.move_id.partner_id.id,r.product_id.categ_id.id))
    def check_validaty(self):
        if (self.date_from and not(self.date_to)) or (self.date_to and not(self.date_from)):
            raise ValidationError(_("please choose date from and date to or don't choose dates at all"))
        if self.date_from > self.date_to:
            raise ValidationError(_("You can't choose date from after date to"))                 
        return True
    def print_report(self):
        lines = self.get_lines()
        if len(lines) == 0:
            raise ValidationError('No Data to show')
        return self.env.ref('invoicing_report.invoicing_reprot').with_context(landscape = True).report_action(lines, data={})
    