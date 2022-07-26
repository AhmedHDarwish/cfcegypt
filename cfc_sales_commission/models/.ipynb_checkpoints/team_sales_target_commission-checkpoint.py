# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class TeamSalesTarget(models.AbstractModel):
    _inherit = 'abstract.sales.target'

    sales_invoices_commission_count = fields.Integer(string='Commissions', compute='get_commissions_count')

    sales_invoices_deduction_count = fields.Integer(string='Deductions', compute='get_deductions_count')
    sh_visible_commision_button = fields.Boolean(compute='_compute_sh_visible_commision_button')
    sh_visible_commision_button_hundred = fields.Boolean(compute='_compute_sh_visible_commision_button_hundred')

    def _compute_sh_visible_commision_button(self):
        for rec in self:
            rec.sh_visible_commision_button = False
            if rec.personal_target_ids:
                target_ids = len(rec.personal_target_ids.ids)
                reached_lines = []
                hundred_lines = []
                for line in rec.personal_target_ids:
                    if line.target_reached >= 80:
                        reached_lines.append(line.id)
                    if line.target_reached >= 100:
                        hundred_lines.append(line.id)

                if target_ids == len(reached_lines):
                    rec.sh_visible_commision_button = True
                if target_ids == len(hundred_lines):
                    rec.sh_visible_commision_button = False
    
    def _compute_sh_visible_commision_button_hundred(self):
        for rec in self:
            rec.sh_visible_commision_button_hundred = False
            if rec.personal_target_ids:
                target_ids = len(rec.personal_target_ids.ids)
                reached_lines = []
                for line in rec.personal_target_ids:
                    if line.target_reached >= 100:
                        reached_lines.append(line.id)
                if target_ids == len(reached_lines):
                    rec.sh_visible_commision_button_hundred = True


    def get_commissions_count(self):
        for rec in self:
            count = self.env['sh.sale.commision.model'].search_count([
                ('type','=','commission'),
                ('team_id','=',rec.crm_team_id.id),
                ('team_leader', '=', rec.crm_team_id.user_id.id),
                ('payment_date','>=',rec.start_date),
                ('payment_date','<=',rec.end_date),
            ])
            print("\n\n\n\ncount",count)
        # count = self.env['account.move'].search_count([
        #                                                 # ('invoice_user_id', 'in', self.personal_target_ids.sale_person_id.ids),
        #                                                 ('invoice_user_id', 'in', self.personal_target_ids.sale_person_id.ids),
        #                                                 ('sh_due_date','>=',self.start_date),
        #                                                 ('sh_due_date','<=',self.end_date),
        #                                                 # ('invoice_date', '>=', self.start_date),
        #                                                 # ('invoice_date', '<=', self.end_date),
        #                                                ('paid_amount', '!=', 0)])
            rec.sales_invoices_commission_count = count

    def get_deductions_count(self):
        for rec in self:
            with_payemnt_count = self.env['sh.sale.commision.model'].search_count([('type','=','deduction'),('team_id','=',rec.crm_team_id.id),('team_leader', '=', rec.crm_team_id.user_id.id),('payment_date','>=',rec.start_date),('payment_date','<=',rec.end_date)])
            without_payment_count = self.env['sh.sale.commision.model'].search_count([('type','=','deduction'),('team_id','=',rec.crm_team_id.id),('team_leader', '=', rec.crm_team_id.user_id.id),('payment_date','=',False),('due_date','>=',rec.start_date),('due_date','<=',rec.end_date)])
            count = with_payemnt_count + without_payment_count
        # count = self.env['account.move'].search_count([
        #                                             # ('invoice_user_id', 'in', self.personal_target_ids.sale_person_id.ids),
        #                                                 ('invoice_user_id', 'in', self.personal_target_ids.sale_person_id.ids),
        #                                                 ('sh_due_date','>=',self.start_date),
        #                                                 ('sh_due_date','<=',self.end_date),
        #                                                 # ('invoice_date_due', '>=', self.start_date),
        #                                                 # ('invoice_date_due', '<=', self.end_date),
        #                                                 # ('invoice_date_due', '<=', fields.Date.today()),
        #                                                 ('sale_person_deduction','!=',0)])
        #                                                 # ('amount_residual', '!=', 0)])
            rec.sales_invoices_deduction_count = count




    def action_view_eighty_commission(self):
        commission_tree = self.env.ref('cfc_sales_commission.sh_leader_commission_eighty_tree_view')
        # commission_tree = self.env.ref('cfc_sales_commission.view_invoice_eighty_commission_tree')
        commission_form = self.env.ref('cfc_sales_commission.sh_leader_eighty_commission_form_view')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payments with Commission'),
            'res_model': 'sh.sale.commision.model',
            'view_mode': 'tree,form',
            'views': [(commission_tree.id, 'tree'),(commission_form.id, 'form')],
            # 'views': [[commission_tree.id, 'list']],
            'domain': [
                    ('team_id.user_id', '=', self.crm_team_id.user_id.id),
                    # ('invoice_user_id', '=', self.personal_target_ids.sale_person_id.ids),
                        ('payment_date','>=',self.start_date),
                        ('payment_date','<=',self.end_date),
                        ('type','=','commission'),
                        # ('invoice_date', '>=', self.start_date),
                        # ('invoice_date', '<=', self.end_date),
                       # ('paid_amount', '!=', 0),
                       # ('type', '=', 'out_invoice')
                       ],
        }

    def action_view_hundred_commission(self):
        commission_tree = self.env.ref('cfc_sales_commission.sh_leader_commission_hundred_tree_view')
        commission_form = self.env.ref('cfc_sales_commission.sh_leader_hundred_commission_form_view')
        # commission_tree = self.env.ref('cfc_sales_commission.view_invoice_hundred_commission_tree')
        # commission_form = self.env.ref('account.view_move_form')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payments with Commission'),
            'res_model': 'sh.sale.commision.model',
            'view_mode': 'tree,form',
            'views': [(commission_tree.id, 'tree'),(commission_form.id, 'form')],
            'domain': [
                    ('team_id.user_id', '=', self.crm_team_id.user_id.id),
                    ('payment_date','>=',self.start_date),
                    ('payment_date','<=',self.end_date),
                    ('type','=','commission'),
                   ],
            # 'domain': [
            #             # ('invoice_user_id', '=', self.personal_target_ids.sale_person_id.ids),
            #             ('invoice_user_id', 'in', self.personal_target_ids.sale_person_id.ids),
            #             ('sh_due_date','>=',self.start_date),
            #             ('sh_due_date','<=',self.end_date),
            #             # ('invoice_date', '>=', self.start_date),
            #             # ('invoice_date', '<=', self.end_date),
            #            ('paid_amount', '!=', 0),
            #            ('type', '=', 'out_invoice')],
        }
    def action_view_deduction(self):
        # deduction_tree = self.env.ref('cfc_sales_commission.view_invoice_deduction_tree')
        # deduction_form = self.env.ref('account.view_move_form')
        deduction_tree = self.env.ref('cfc_sales_commission.sh_leader_deduction_tree_view')
        deduction_form = self.env.ref('cfc_sales_commission.sh_leader_deduction_form_view')
        with_payemnt_count = self.env['sh.sale.commision.model'].search([('type','=','deduction'),('team_id','=',self.crm_team_id.id),('team_leader', '=', self.crm_team_id.user_id.id),('payment_date','>=',self.start_date),('payment_date','<=',self.end_date)]).ids
        without_payment_count = self.env['sh.sale.commision.model'].search([('type','=','deduction'),('team_id','=',self.crm_team_id.id),('team_leader', '=', self.crm_team_id.user_id.id),('payment_date','=',False),('due_date','>=',self.start_date),('due_date','<=',self.end_date)]).ids
        invoice_ids = with_payemnt_count + without_payment_count
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payments with Deduction'),
            'res_model': 'sh.sale.commision.model',
            'view_mode': 'tree,form',
            'views': [(deduction_tree.id, 'tree'),(deduction_form.id, 'form')],
            'domain': [('id','in',invoice_ids)],
            # 'domain': [
            #             ('invoice_user_id', 'in', self.personal_target_ids.sale_person_id.ids),
            #             # ('invoice_user_id', '=', self.personal_target_ids.sale_person_id.ids),
            #             ('sh_due_date','>=',self.start_date),
            #             ('sh_due_date','<=',self.end_date),
            #             # ('invoice_date_due', '>=', self.start_date),
            #             # ('invoice_date_due', '<=', self.end_date),
            #             # ('invoice_date_due', '<=', fields.Date.today()),
            #             ('sale_person_deduction','!=',0),
            #             # ('amount_residual', '!=', 0),
            #            ('type', '=', 'out_invoice')],
        }

class PersonalSalesTarget(models.Model):
    _inherit = 'personal.sales.target'

    def action_view_sale_person_hundred_commission(self):
        # commission_tree = self.env.ref('cfc_sales_commission.view_invoice_sale_person_hundred_commission_tree')
        # commission_form = self.env.ref('account.view_move_form')
        commission_tree = self.env.ref('cfc_sales_commission.sh_person_commission_hundred_tree_view')
        commission_form = self.env.ref('cfc_sales_commission.sh_person_hundred_commission_form_view')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payments with Commission'),
            'res_model': 'sh.sale.commision.model',
            'view_mode': 'tree,form',
            'views': [(commission_tree.id, 'tree'), (commission_form.id, 'form')],
            'domain': [
                    ('team_id','=',self.team_target_id.crm_team_id.id),
                    ('user_id', '=',self.sale_person_id.id),
                    ('payment_date','>=',self.start_date),
                    ('payment_date','<=',self.end_date),
                    ('type','=','commission'),
                   ],
            # 'domain': [('invoice_user_id', '=', self.sale_person_id.id),
            #             ('sh_due_date','>=',self.start_date),
            #             ('sh_due_date','<=',self.end_date),
            #             # ('invoice_date', '>=', self.start_date),
            #             # ('invoice_date', '<=', self.end_date),
            #            ('paid_amount', '!=', 0),
            #            ('type', '=', 'out_invoice')],
        }

    def action_view_sale_person_eighty_commission(self):
        # commission_tree = self.env.ref('cfc_sales_commission.view_invoice_sale_person_eighty_commission_tree')
        # commission_form = self.env.ref('account.view_move_form')
        commission_tree = self.env.ref('cfc_sales_commission.sh_person_commission_eighty_tree_view')
        commission_form = self.env.ref('cfc_sales_commission.sh_person_eighty_commission_form_view')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payments with Commission'),
            'res_model': 'sh.sale.commision.model',
            'view_mode': 'tree,form',
            'views': [(commission_tree.id, 'tree'), (commission_form.id, 'form')],
            'domain': [
                    ('team_id','=',self.team_target_id.crm_team_id.id),
                    ('user_id', '=',self.sale_person_id.id),
                    ('payment_date','>=',self.start_date),
                    ('payment_date','<=',self.end_date),
                    ('type','=','commission'),
                   ],
            # 'domain': [('invoice_user_id', '=', self.sale_person_id.id),
            #             ('sh_due_date','>=',self.start_date),
            #             ('sh_due_date','<=',self.end_date),
            #             # ('invoice_date', '>=', self.start_date),
            #             # ('invoice_date', '<=', self.end_date),
            #            ('paid_amount', '!=', 0),
            #            ('type', '=', 'out_invoice')],
        }
    