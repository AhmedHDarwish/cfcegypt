from odoo import models, api,fields,_
from datetime import datetime


class PersonalSalesTarget(models.Model):
    _inherit = 'personal.sales.target'

    # commision_ids = fields.Many2many('sh.sale.commision.model',string='Commisions')
    # sh_commision_ids = fields.Many2many('account.move',string='Commisions',compute='_compute_commissions')
    # deduction_ids = fields.Many2many('account.move',string='Deductions',compute='_compute_deductions')
    
    sh_person_commision_count = fields.Integer(string='Commissions',compute='_compute_person_commissions')
    sh_person_deduction_count = fields.Integer(string='Commissions',compute='_compute_person_deductions')
    
    def _compute_person_commissions(self):
        for rec in self:
            commission_count = self.env['sh.sale.commision.model'].search_count([
                ('team_id','=',rec.team_target_id.crm_team_id.id),
                ('user_id', '=',self.sale_person_id.id),
                ('payment_date','>=',self.start_date),
                ('payment_date','<=',self.end_date),
                ('type','=','commission'),
            ])
            rec.sh_person_commision_count = commission_count

    def action_view_person_commisions(self):
        commission_tree = self.env.ref('cfc_sales_commission.sh_person_commission_eighty_tree_view')
        commission_form = self.env.ref('cfc_sales_commission.sh_person_eighty_commission_form_view')
        if self.invoiced_target_reached >= 100: 
            commission_tree = self.env.ref('cfc_sales_commission.sh_person_commission_hundred_tree_view')
            commission_form = self.env.ref('cfc_sales_commission.sh_person_hundred_commission_form_view')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payments with Commissions'),
            'res_model': 'sh.sale.commision.model',
            'view_mode': 'tree,form',
            'views': [(commission_tree.id, 'tree'),(commission_form.id, 'form')],
            'domain': [
                    ('team_id','=',self.team_target_id.crm_team_id.id),
                    ('user_id', '=',self.sale_person_id.id),
                    ('payment_date','>=',self.start_date),
                    ('payment_date','<=',self.end_date),
                    ('type','=','commission'),
                   ],
            }

    def _compute_person_deductions(self):
        for rec in self:
            with_payemnt_count = self.env['sh.sale.commision.model'].search_count([('type','=','deduction'),('team_id','=',rec.team_target_id.crm_team_id.id),('user_id', '=', rec.sale_person_id.id),('payment_date','>=',rec.start_date),('payment_date','<=',rec.end_date)])
            without_payment_count = self.env['sh.sale.commision.model'].search_count([('type','=','deduction'),('team_id','=',rec.team_target_id.crm_team_id.id),('user_id', '=', rec.sale_person_id.id),('payment_date','=',False),('due_date','>=',rec.start_date),('due_date','<=',rec.end_date)])
            deduction_count = with_payemnt_count + without_payment_count
            rec.sh_person_deduction_count = deduction_count
    
    def action_view_person_deductions(self):
        deduction_tree = self.env.ref('cfc_sales_commission.sh_leader_deduction_tree_view')
        deduction_form = self.env.ref('cfc_sales_commission.sh_person_deduction_form_view')
        with_payemnt_count = self.env['sh.sale.commision.model'].search([('type','=','deduction'),('team_id','=',self.team_target_id.crm_team_id.id),('user_id', '=', self.sale_person_id.id),('payment_date','>=',self.start_date),('payment_date','<=',self.end_date)]).ids
        without_payment_count = self.env['sh.sale.commision.model'].search([('type','=','deduction'),('team_id','=',self.team_target_id.crm_team_id.id),('user_id', '=', self.sale_person_id.id),('payment_date','=',False),('due_date','>=',self.start_date),('due_date','<=',self.end_date)]).ids
        invoice_ids = with_payemnt_count + without_payment_count
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payments with Deductions'),
            'res_model': 'sh.sale.commision.model',
            'view_mode': 'tree,form',
            'views': [(deduction_tree.id, 'tree'),(deduction_form.id, 'form')],
            'domain': [
                    ('id','in',invoice_ids),
                   ],
            }
    
    # def _compute_commissions(self):
    #     if self:
    #         for rec in self:
    #             rec.commision_ids = False
    #             rec.sh_commision_ids = False
    #             commision_ids = self.env['account.move'].search([
    #                 ('invoice_user_id', '=', rec.sale_person_id.id),
    #                 # ('invoice_date', '>=', rec.start_date),
    #                 # ('invoice_date', '<=', rec.end_date),
    #                 ('sh_due_date','>=',rec.start_date),
    #                 ('sh_due_date','<=',rec.end_date),
    #                 ('paid_amount', '!=', 0),
    #                 ('type', '=', 'out_invoice'),
    #                 ('company_id','in',self.env.companies.ids)
    #             ])
    #             if commision_ids:
    #                 rec.commision_ids =[(6,0,commision_ids.ids)]
    #                 rec.sh_commision_ids =[(6,0,commision_ids.ids)]
    #
    # def _compute_deductions(self):
    #     if self:
    #         for rec in self:
    #             rec.deduction_ids = False
    #             deduction_ids = self.env['account.move'].sudo().search([
    #                 ('invoice_user_id', '=', rec.sale_person_id.id),
    #                 # ('invoice_date_due', '>=', rec.start_date),
    #                 # ('invoice_date_due', '<=', rec.end_date),
    #                 # ('invoice_date_due', '<=', fields.Date.today()),
    #                 ('sh_due_date','>=',rec.start_date),
    #                 ('sh_due_date','<=',rec.end_date),
    #                 ('sale_person_deduction', '!=', 0),
    #                 ('company_id','in',self.env.companies.ids)
    #             ])
    #             if deduction_ids:
    #                 rec.deduction_ids =[(6,0,deduction_ids.ids)]
