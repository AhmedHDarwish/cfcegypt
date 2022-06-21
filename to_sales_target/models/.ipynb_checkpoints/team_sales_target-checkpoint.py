from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools.misc import format_date
import json
import datetime


class TeamSalesTarget(models.Model):
    _name = 'team.sales.target'
    _inherit = 'abstract.sales.target'
    _description = 'Team Sales Target'
    _rec_name = 'crm_team_id'

    crm_team_id = fields.Many2one('crm.team', string='Sales Team', required=True, index=True,
                                  readonly=True, states={'draft': [('readonly', False)]})

    personal_target_ids = fields.One2many('personal.sales.target', 'team_target_id', string='Personal Sales Targets',
                                          help="Sales targets for the team members which will be suggested automatically on changing the Sales Team."
                                          " Please remember to add member to the team first to have the targets suggested.",
                                          readonly=True, states={'draft': [('readonly', False)]}, compute="_compute_personal_target_ids", store=True)
    # target_commision_ids = fields.Many2many('sh.sale.commision.model','rel_team_target_commision_model',string='Commission')
    # target_deduction_ids = fields.Many2many('sh.sale.commision.model','rel_team_target_commision_model_deduction',string='Deduction')

    @api.constrains('start_date', 'end_date', 'crm_team_id')
    def _check_overlapping(self):
        TeamTarget = self.env['team.sales.target']
        for r in self:
            overlap = TeamTarget.search([('crm_team_id', '=', r.crm_team_id.id), ('id', '!=', r.id),
                                         ('start_date', '<=', r.end_date),
                                         ('end_date', '>=', r.start_date)], limit=1)
            if overlap:
                raise ValidationError(_("The target you've input is overlapping an existing one which has Date Start: %s, Date End: %s")
                                      % (overlap.start_date, overlap.end_date))

    def _prepare_personal_target_data(self, user, target):
        return {
            'sale_person_id': user.id,
            'team_target_id': self.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'target': target,
            'state': self.state,
            }
    
    def action_generate_commision(self):

        self.ensure_one()
        commissions = self.env['sh.sale.commision.model'].sudo().search([('type','=','commission')])
        deductions = self.env['sh.sale.commision.model'].sudo().search([('type','=','deduction')])
        if commissions:
            commissions.unlink()
        if deductions:
            deductions.unlink()
        payment_ids = self.env['account.payment'].sudo().search([('payment_date','>=',self.start_date),('payment_date','<=',self.end_date),('payment_type','=','inbound')])
        if payment_ids:
            for payment in payment_ids:
                if payment.reconciled_invoice_ids:
                    for invoice in payment.reconciled_invoice_ids:
                        if invoice.move_type == 'out_invoice':
                            payment_last_date = invoice.sh_due_date
                            if payment_last_date:
                                team_target_reached = self.invoiced_target_reached
                                if invoice.invoice_line_ids:
                                    str_type_dictt = invoice.invoice_payments_widget
                                    dictt = json.loads(str_type_dictt)
                                    if dictt and 'content' in dictt:
                                        content = dictt.get('content')
                                        for dictt in content:
                                            datetime_obj = datetime.datetime.strptime(dictt.get('date'), "%Y-%m-%d")
                                            if datetime_obj.date() <= payment_last_date:
                                                commission_vals = {
                                                    'type':'commission',
                                                    'invoice_ref':invoice.id,
                                                    'partner_id':invoice.partner_id.id,
                                                    'invoice_date':invoice.invoice_date,
                                                    'source_document':invoice.invoice_origin,
                                                    'team_id':invoice.team_id.id,
                                                    'team_leader':invoice.team_leader.id,
                                                    'user_id':invoice.invoice_user_id.id,
                                                    'company_id':invoice.company_id.id,
                                                    'due_date':invoice.sh_due_date,
                                                    'payment_date':datetime_obj,
                                                    'invoice_total':invoice.amount_total
                                                }
                                                amount_tax =  0.0
                                                payment_amount = 0.0
                                                if dictt.get('amount') > 0.0:
                                                    amount_tax = invoice.amount_tax * dictt.get('amount') / invoice.amount_total
                                                payment_amount = dictt.get('amount') - amount_tax
                                                commission_vals.update({
                                                    'payment_amount':dictt.get('amount')
                                                    })
                                                if team_target_reached >= 80 and team_target_reached < 100:
                                                    leader_eighty_percent_commission = invoice.invoice_line_ids[0].product_id.categ_id.team_lead_eighty_percent
                                                    leader_eighty_percent_commission_value = leader_eighty_percent_commission * payment_amount
                                                    
                                                    commission_vals.update({
                                                        'leader_eighty_percentage':leader_eighty_percent_commission,
                                                        'leder_eighty_commission_amount':leader_eighty_percent_commission_value
                                                    })
                                                if team_target_reached >= 100:
                                                    leader_hundred_percent_commission = invoice.invoice_line_ids[0].product_id.categ_id.team_lead_hundred_percent
                                                    leader_hundred_percent_commission_value = leader_hundred_percent_commission * payment_amount
                                                    commission_vals.update({
                                                        'leader_hundred_percentage':leader_hundred_percent_commission,
                                                        'leder_hundred_commission_amount':leader_hundred_percent_commission_value
                                                    })
                                                if self.personal_target_ids:
                                                    for personal_target in self.personal_target_ids:
                                                        personal_target_reached = personal_target.target_reached
                                                        if personal_target_reached >= 80 and personal_target_reached < 100:
                                                            person_eighty_percent_commission = invoice.invoice_line_ids[0].product_id.categ_id.sale_person_eighty_percent
                                                            person_eighty_percent_commission_value = person_eighty_percent_commission * payment_amount
                                                            commission_vals.update({
                                                                'saleperson_eighty_percentage':person_eighty_percent_commission,
                                                                'saleperson_eighty_commission_amount':person_eighty_percent_commission_value
                                                            })
                                                        if personal_target_reached >= 100:
                                                            person_hundred_percent_commission = invoice.invoice_line_ids[0].product_id.categ_id.sale_person_hundred_percent
                                                            person_hundred_percent_commission_value = person_hundred_percent_commission * payment_amount
                                                            commission_vals.update({
                                                                'saleperson_hundred_percentage':person_hundred_percent_commission,
                                                                'saleperson_hundred_commission_amount':person_hundred_percent_commission_value
                                                            })
                                                if commission_vals:
                                                    commission_id = self.env['sh.sale.commision.model'].sudo().create(commission_vals)
                                            # elif datetime_obj.date() > payment_last_date:
                                            #     deduction_vals = {
                                            #         'type':'deduction',
                                            #         'invoice_ref':invoice.id,
                                            #         'partner_id':invoice.partner_id.id,
                                            #         'invoice_date':invoice.invoice_date,
                                            #         'source_document':invoice.invoice_origin,
                                            #         'team_id':invoice.team_id.id,
                                            #         'team_leader':invoice.team_leader.id,
                                            #         'user_id':invoice.invoice_user_id.id,
                                            #         'company_id':invoice.company_id.id,
                                            #         'due_date':invoice.sh_due_date,
                                            #         'invoice_total':invoice.amount_total,
                                            #         'deduction_amount':dictt.get('amount'),
                                            #         'payment_amount':dictt.get('amount'),
                                            #         'payment_date':datetime_obj
                                            #     }
                                            #     if deduction_vals:
                                            #         deduction_id = self.env['sh.sale.commision.model'].sudo().create(deduction_vals)
        deduction_invoice_ids = self.env['account.move'].sudo().search([
            ('invoice_date','>=',self.start_date),
            ('invoice_date','<=',self.end_date),
            ('move_type','=','out_invoice'),
            ('team_id','=',self.crm_team_id.id),
            ('team_leader','=',self.crm_team_id.user_id.id),
            ('state','=','posted'),
            ('amount_residual','>',0.0)
        ])
        if deduction_invoice_ids:
            for deduction_invoice in deduction_invoice_ids:                
                if deduction_invoice.sh_due_date > self.start_date and deduction_invoice.sh_due_date < self.end_date:                
                    deduction_id = self.env['sh.sale.commision.model'].sudo().search([
                        ('type','=','deduction'),
                        ('invoice_ref','=',deduction_invoice.id),
                        ('deduction_amount','=',deduction_invoice.amount_total),
                    ])
                    if not deduction_id:
                        deduction_vals = {
                            'type':'deduction',
                            'invoice_ref':deduction_invoice.id,
                            'partner_id':deduction_invoice.partner_id.id,
                            'invoice_date':deduction_invoice.invoice_date,
                            'source_document':deduction_invoice.invoice_origin,
                            'team_id':deduction_invoice.team_id.id,
                            'team_leader':deduction_invoice.team_leader.id,
                            'user_id':deduction_invoice.invoice_user_id.id,
                            'company_id':deduction_invoice.company_id.id,
                            'due_date':deduction_invoice.sh_due_date,
                            'invoice_total':deduction_invoice.amount_total,
                            'deduction_amount':deduction_invoice.amount_residual,
                        }
                        dedution_id = self.env['sh.sale.commision.model'].sudo().create(deduction_vals)

    @api.depends('crm_team_id','target')
    def _compute_personal_target_ids(self):
        for r in self:        
            if r.crm_team_id:
            # compute personal target by equal dividing
                if not r.crm_team_id.member_ids:
                    personal_target = 0.0
                else:
                    personal_target = r.target / len(r.crm_team_id.member_ids)
    
                personal_target_ids = r.env['personal.sales.target']
                for member in r.crm_team_id.member_ids:
                    # check if there is an existing line, then use it.
                    if r._origin.id > 0:
                        existing_line = personal_target_ids.search([('sale_person_id', '=', member.id), ('team_target_id', '=', r._origin.id)], limit=1)
                        if existing_line:
                            personal_target_ids += existing_line
                            continue
                    # no existing line, create a new one.
                    new_line = personal_target_ids.new(r._prepare_personal_target_data(member, personal_target))
                    personal_target_ids += new_line
                r.personal_target_ids = personal_target_ids
            else:
                r.personal_target_ids = False

    def subscribe_team_leader(self):
        for r in self:
            subscribers = []
            if r.crm_team_id:
                if r.crm_team_id.user_id and r.crm_team_id.user_id.partner_id.id not in r.message_follower_ids.ids:
                    subscribers += [r.crm_team_id.user_id.partner_id.id]
            if subscribers:
                r.message_subscribe(subscribers)

    def subscribe_approvers(self):
        for r in self:
            subscribers = []
            if r.crm_team_id:
                if r.crm_team_id.regional_manager_id and r.crm_team_id.regional_manager_id.partner_id.id not in r.message_follower_ids.ids:
                    subscribers += [r.crm_team_id.regional_manager_id.partner_id.id]
            if subscribers:
                r.message_subscribe(subscribers)

    def action_confirm(self):
        self.mapped('personal_target_ids').action_confirm()
        super(TeamSalesTarget, self).action_confirm()
        self.subscribe_approvers()

    def action_compute(self):
        target_all = 0.0
        for rec in self.personal_target_ids:
            person_target = 0.0
            lead_ids = self.env['crm.lead'].search([('user_id', '=', rec.sale_person_id.id),
                                                    ('date_deadline', '<=', self.end_date),
                                                    ('date_deadline', '>=', self.start_date)])
            for lead_id in lead_ids:
                person_target += lead_id.planned_revenue
            rec.target = person_target
            target_all += person_target
        self.target = target_all

    def action_draft(self):
        self.mapped('personal_target_ids').action_draft()
        super(TeamSalesTarget, self).action_draft()

    def action_refuse(self):
        is_regional_sales_manager = self.env.user.has_group('sales_team.group_sale_salesman_all_leads')
        for r in self:
            if not is_regional_sales_manager:
                raise ValidationError(_("You must be granted with Regional Sales Manager access rights"
                                        " to refuse the sales target for the sales team '%s'")
                                        % (r.crm_team_id.name,))
            if r.personal_target_ids:
                r.personal_target_ids.action_refuse()
        super(TeamSalesTarget, self).action_refuse()

    def action_approve(self):
        is_regional_sales_manager = self.env.user.has_group('sales_team.group_sale_salesman_all_leads')
        for r in self:
            if not is_regional_sales_manager:
                raise ValidationError(_("You must be granted with Regional Sales Manager access rights"
                                        " to approve the sales target for the sales team '%s'")
                                        % (r.crm_team_id.name,))
            if r.personal_target_ids:
                r.personal_target_ids.action_approve()
        super(TeamSalesTarget, self).action_approve()

    def action_cancel(self):
        self.mapped('personal_target_ids').action_cancel()
        super(TeamSalesTarget, self).action_cancel()

    @api.model_create_multi
    def create(self, vals_list):
        records = super(TeamSalesTarget, self).create(vals_list)
        records.subscribe_team_leader()
        return records

    def write(self, vals):
        if 'crm_team_id' in vals:
            for r in self:
                unsubscribers = []
                if r.crm_team_id.user_id:
                    unsubscribers += [r.crm_team_id.user_id.partner_id.id]

                if unsubscribers:
                    r.message_unsubscribe(unsubscribers)
        res = super(TeamSalesTarget, self).write(vals)
        if 'crm_team_id' in vals:
            self.subscribe_team_leader()
        return res

    def _build_name(self):
        return "%s [%s] [%s ~ %s]" % (self.crm_team_id.name, self.target, format_date(self.env, self.start_date), format_date(self.env, self.end_date))

    def name_get(self):
        result = []
        for r in self:
            result.append((r.id, r._build_name()))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('crm_team_id.name', 'ilike', name + '%'), ('name', operator, name)]
        tags = self.search(domain + args, limit=limit)
        return tags.name_get()
    
