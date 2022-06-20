# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import timedelta
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
import operator as py_operator

OPERATORS = {
    '<': py_operator.lt,
    '>': py_operator.gt,
    '<=': py_operator.le,
    '>=': py_operator.ge,
    '=': py_operator.eq,
    '!=': py_operator.ne
}

class AccountMove(models.Model):
    _inherit = 'account.move'

    team_leader = fields.Many2one(string="Team Leader",related="team_id.user_id", store=True)

    team_leader_eighty_percent = fields.Float("Leader Percentage", compute="_compute_team_leader_eighty_percent_commission", digits=(12,6))

    team_leader_hundred_percent = fields.Float("Leader Percentage", compute="_compute_team_leader_hundred_percent_commission", digits=(12,6))

    sale_person_eighty_percent = fields.Float("Sales Person Percentage", compute="_compute_sale_person_eighty_percent_commission", digits=(12,6))

    sale_person_hundred_percent = fields.Float("Sales Person Percentage", compute="_compute_sale_person_hundred_percent_commission", digits=(12,6))

    paid_amount = fields.Float("Paid Amount", compute='_compute_paid_amount', store=True, readonly=True)


    sale_person_eighty_percent_commission_value = fields.Float("Sale Person 80% Commission",compute="_compute_sale_person_eighty_percent_commission", store=True, readonly=True)

    sale_person_hundred_percent_commission_value = fields.Float(string="Sale Person 100% Commission",compute="_compute_sale_person_hundred_percent_commission", store=True, readonly=True)

    team_leader_eighty_percent_commission_value = fields.Float(string="Team Leader 80% Commission",compute="_compute_team_leader_eighty_percent_commission", store=True, readonly=True)
    team_leader_hundred_percent_commission_value = fields.Float(string="Team Leader 100% Commission",compute="_compute_team_leader_hundred_percent_commission", store=True, readonly=True)

    sale_person_deduction = fields.Float(string="Sale Person Deduction", compute="_compute_sale_person_deduction",search='_search_sale_person_deduction')
    sh_due_date = fields.Date('Payment Last Date',compute='_compute_sh_due_date',search='_search_sh_due_date')
    sh_paid_amount_for_commision = fields.Float(compute="_compute_sale_person_deduction",string='Valid Commissions Amount')
    
    def _compute_sh_due_date(self):
        for rec in self:
            if rec.invoice_date_due:
                if rec.partner_id.credit_days:
                    allow_date = rec.invoice_date_due + timedelta(days=int(rec.partner_id.credit_days))
                    if allow_date:
                        rec.sh_due_date = allow_date
                else:
                    rec.sh_due_date = rec.invoice_date_due
            else:
                rec.sh_due_date = False
    
    def _search_sale_person_deduction(self,operator,value):
        # TDE FIXME: should probably clean the search methods
        # to prevent sql injections
        if operator not in ('<', '>', '=', '!=', '<=', '>='):
            raise UserError(_('Invalid domain operator %s') % operator)
        # TODO: Still optimization possible when searching virtual quantities
        ids = []
        # Order the search on `id` to prevent the default order on the product name which slows
        # down the search because of the join on the translation table to get the translated names.
        for move in self.sudo().with_context(prefetch_fields=False).sudo().search([], order='id'):
            if OPERATORS[operator](move['sale_person_deduction'], value):
                ids.append(move.id)
        return [('id', 'in', ids)]
    
    def _search_sh_due_date(self, operator, value):
        moves = self.env['account.move'].sudo().search([])
        records = []
        for move in moves:
            if move.invoice_date_due:
                if move.partner_id.credit_days:
                    allow_date = move.sh_due_date - timedelta(days=int(move.partner_id.credit_days))
                    if allow_date:
                        records.append(move.id)
        return [('id', 'in', records)]

    @api.depends('amount_residual', 'amount_total')
    def _compute_paid_amount(self):
        for rec in self:
            rec.paid_amount = rec.amount_total - rec.amount_residual

    def _compute_sale_person_deduction(self):
        for rec in self:
            foreign_currency = rec.currency_id if rec.currency_id != rec.company_id.currency_id else False
            pay_term_line_ids = rec.line_ids.sudo().filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
            partials = pay_term_line_ids.mapped('matched_debit_ids') + pay_term_line_ids.mapped('matched_credit_ids')
            payment_amount = 0.0
            deduction_amount = 0.0
            rec.sale_person_deduction = float(rec.amount_residual)
            for partial in partials:
                counterpart_lines = partial.debit_move_id + partial.credit_move_id
                counterpart_line = counterpart_lines.sudo().filtered(lambda line: line.id not in rec.line_ids.ids)
                # In case we are in an onchange, line_ids is a NewId, not an integer. By using line_ids.ids we get the correct integer value.
                if foreign_currency and partial.currency_id == foreign_currency:
                    amount = partial.amount_currency
                else:
                    amount = partial.company_currency_id._convert(partial.amount, rec.currency_id, rec.company_id, rec.date)
                if rec.sh_due_date:
                    if counterpart_line.date > rec.sh_due_date:
                        deduction_amount+=amount
                    else:
                        payment_amount+=amount
            if deduction_amount > 0.0:
                rec.sale_person_deduction = deduction_amount
            amount_tax =  0.0
            if payment_amount > 0.0:
                amount_tax = rec.amount_tax * payment_amount / rec.amount_total
            rec.sh_paid_amount_for_commision = payment_amount - amount_tax

    @api.depends('amount_residual', 'amount_untaxed')
    def _compute_team_leader_eighty_percent_commission(self):
        for rec in self:
            rec.team_leader_eighty_percent_commission_value = 0
            if rec.invoice_line_ids:
                eighty_percent_commission = rec.invoice_line_ids[0].product_id.categ_id.team_lead_eighty_percent
                rec.team_leader_eighty_percent = eighty_percent_commission
                rec.team_leader_eighty_percent_commission_value = eighty_percent_commission * rec.sh_paid_amount_for_commision
                # rec.team_leader_eighty_percent_commission_value = eighty_percent_commission * (rec.amount_untaxed - rec.amount_residual)

    @api.depends('amount_residual', 'amount_untaxed')
    def _compute_sale_person_eighty_percent_commission(self):
        for rec in self:
            rec.sale_person_eighty_percent_commission_value = 0
            if rec.invoice_line_ids:
                eighty_percent_commission = rec.invoice_line_ids[0].product_id.categ_id.sale_person_eighty_percent
                rec.sale_person_eighty_percent = eighty_percent_commission
                rec.sale_person_eighty_percent_commission_value = eighty_percent_commission * rec.sh_paid_amount_for_commision
                # rec.sale_person_eighty_percent_commission_value = eighty_percent_commission * (rec.amount_untaxed - rec.amount_residual)

    @api.depends('amount_residual', 'amount_untaxed')
    def _compute_team_leader_hundred_percent_commission(self):
        for rec in self:
            rec.team_leader_hundred_percent_commission_value = 0
            if rec.invoice_line_ids:
                hundred_percent_commission = rec.invoice_line_ids[0].product_id.categ_id.team_lead_hundred_percent
                rec.team_leader_hundred_percent = hundred_percent_commission
                rec.team_leader_hundred_percent_commission_value = hundred_percent_commission * rec.sh_paid_amount_for_commision
                # rec.team_leader_hundred_percent_commission_value = hundred_percent_commission * (rec.amount_untaxed - rec.amount_residual)

    @api.depends('amount_residual', 'amount_untaxed')
    def _compute_sale_person_hundred_percent_commission(self):
        for rec in self:
            rec.sale_person_hundred_percent_commission_value = 0
            if rec.invoice_line_ids:
                hundred_percent_commission = rec.invoice_line_ids[0].product_id.categ_id.sale_person_hundred_percent
                rec.sale_person_hundred_percent = hundred_percent_commission
                rec.sale_person_hundred_percent_commission_value = hundred_percent_commission * rec.sudo().sh_paid_amount_for_commision
                # rec.sale_person_hundred_percent_commission_value = hundred_percent_commission * (rec.amount_untaxed - rec.amount_residual)
                