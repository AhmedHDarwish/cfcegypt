# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SalespersonCustomerStatement(models.AbstractModel):
    _name = 'report.sh_customer_statement.sh_spc_statement_report_doc'
    _description = "sale person customer statement report abstract model"  

    @api.model
    def _get_report_values(self, docids, data=None):
        customer_statement_dic = {}
        customer_statement_aging_dic = {} 
        statement_list = []
        partner_statement_obj = self.env['sh.customer.statement']
        partner_overdue_statement_obj = self.env['sh.customer.due.statement']
        if data.get('sh_partner_ids', False):
            for partner_id in data.get('sh_partner_ids'):
                record_list = []
                customer_aging_list = []
                if data.get('sh_report_type') == 'customer_invoice':
                    domain = [
                        ("sh_customer_invoice_date", ">=", data['sh_date_from']),
                        ("sh_customer_invoice_date", "<=", data['sh_date_to']),
                        ("partner_id", "=", partner_id)
                    ]
                    statements = partner_statement_obj.sudo().search(domain)
                    if statements:
                        for statement in statements:
                            statement_dic = {
                                'name' : statement.name,
                                'sh_account'   : statement.sh_account,
                                'sh_customer_invoice_date'     : statement.sh_customer_invoice_date,
                                'sh_customer_due_date'        : statement.sh_customer_due_date,
                                'currency_id':statement.currency_id.symbol,
                                'sh_customer_amount'  : statement.sh_customer_amount,
                                'sh_customer_paid_amount'   : statement.sh_customer_paid_amount,
                                'sh_customer_balance'   : statement.sh_customer_balance,
                                }
                            record_list.append(statement_dic)
                            
                    search_partner = self.env['res.partner'].sudo().search([
                                                ('id', '=', partner_id)
                                                ], limit=1)
                    if search_partner:
                        customer_aging_dic = {
                            'sh_customer_zero_to_thiry':search_partner.sh_customer_zero_to_thiry,
                            'sh_customer_thirty_to_sixty':search_partner.sh_customer_thirty_to_sixty,
                            'sh_customer_sixty_to_ninety':search_partner.sh_customer_sixty_to_ninety,
                            'sh_customer_ninety_plus':search_partner.sh_customer_ninety_plus,
                            'sh_customer_total':search_partner.sh_customer_total,
                            }
                        customer_aging_list.append(customer_aging_dic)
                        customer_statement_aging_dic.update({
                            search_partner.name : customer_aging_list
                            })
                        customer_statement_dic.update({search_partner.name : record_list})
                        statement_list.append(search_partner.name)
                elif data.get('sh_report_type') == 'customer_overdue_invoice':
                    domain = [
                        ("sh_due_customer_invoice_date", ">=", data['sh_date_from']),
                        ("sh_due_customer_invoice_date", "<=", data['sh_date_to']),
                        ("partner_id", "=", partner_id)
                    ]
                    statements = partner_overdue_statement_obj.sudo().search(domain)
                    if statements:
                        for statement in statements:
                            statement_dic = {
                                'name' : statement.name,
                                'sh_account'   : statement.sh_account,
                                'sh_customer_invoice_date'     : statement.sh_due_customer_invoice_date,
                                'sh_customer_due_date'        : statement.sh_due_customer_due_date,
                                'currency_id':statement.currency_id.symbol,
                                'sh_customer_amount'  : statement.sh_due_customer_amount,
                                'sh_customer_paid_amount'   : statement.sh_due_customer_paid_amount,
                                'sh_customer_balance'   : statement.sh_due_customer_balance,
                                }
                            record_list.append(statement_dic)
                            
                    search_partner = self.env['res.partner'].sudo().search([
                                                ('id', '=', partner_id)
                                                ], limit=1)
                    if search_partner:
                        customer_statement_dic.update({search_partner.name : record_list})
                        statement_list.append(search_partner.name)
        data = {
            'date_start': data['sh_date_from'],
            'date_end': data['sh_date_to'],
            'customer_statement_dic' :customer_statement_dic,
            'customer_statement_aging_dic':customer_statement_aging_dic,
            'statement_list' : statement_list,
            'sh_report_type':data['sh_report_type'],
        }        
        return data


class CustomerStatementReportWizard(models.TransientModel):
    _name = 'sh.customer.statement.report.wizard'
    _description = 'Customer Statement Report Wizard'

    sh_report_type = fields.Selection([('customer_invoice','Customer Invoice'),('customer_overdue_invoice','Customer Overdue Invoice')],default='customer_invoice',string='Report Type')
    sh_date_from = fields.Date('From Date', required=True)
    sh_date_to = fields.Date('To Date', required=True)
    sh_partner_ids = fields.Many2many('res.partner',string='Customers', required=True)
    
    @api.constrains('sh_date_from', 'sh_date_to')
    def _check_dates(self):
        if self.filtered(lambda c: c.sh_date_to and c.sh_date_from > c.sh_date_to):
            raise ValidationError(_('Date from must be less than Date to.'))    
    
    def action_print(self):
        datas = self.read()[0]
        return self.env.ref('sh_customer_statement.sh_salesperson_customer_statement_report').report_action([], data=datas)    