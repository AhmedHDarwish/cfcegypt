from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.misc import format_date


class PersonalSalesTarget(models.Model):
    _name = 'personal.sales.target'
    _inherit = 'abstract.sales.target'
    _description = 'Personal Sales Target'
    _rec_name = 'sale_person_id'

    team_target_id = fields.Many2one('team.sales.target', string='Team Sales Target', index=True, required=True, ondelete='cascade',
                                     readonly=True, states={'draft': [('readonly', False)]})
    sale_person_id = fields.Many2one('res.users', string='Sale Person', required=True, index=True,
                                     readonly=True, states={'draft': [('readonly', False)]}, ondelete='cascade')
    
    start_date = fields.Date(related='team_target_id.start_date', store=True)
    end_date = fields.Date(related='team_target_id.end_date', store=True)
    
    _sql_constraints = [
            ('person_unique_per_team',
             'UNIQUE(team_target_id,sale_person_id)',
             "The sales person must be unique per Team Sales Target. You cannot define more than"
             " one personal sales target for the same sales person in the same Team Sales Target"),
        ]

    def action_generate_commision(self):
        self.ensure_one()
        if self.team_target_id:
            self.team_target_id.action_generate_commision()


    @api.constrains('start_date', 'end_date', 'sale_person_id')
    def _check_overlapping(self):
        PersonalTarget = self.env['personal.sales.target']
        for r in self:
            overlap = PersonalTarget.search([
                ('sale_person_id', '=', r.sale_person_id.id),
                ('id', '!=', r.id),
                ('start_date', '<=', r.end_date),
                ('end_date', '>=', r.start_date)], limit=1)
            if overlap:
                raise ValidationError(_("The target you've input for the sales person %s is overlapping an existing one which has Date Start: %s and Date End: %s")
                                       % (r.sale_person_id.name, format_date(self.env, overlap.start_date), format_date(self.env, overlap.end_date)))

    def subscribe_salesperson(self):
        for r in self:
            subscribers = []
            if r.sale_person_id.partner_id.id not in r.message_follower_ids.ids:
                subscribers += [r.sale_person_id.partner_id.id]

            if subscribers:
                r.message_subscribe(subscribers)

    def subscribe_approvers(self):
        for r in self:
            subscribers = []
            if r.sale_person_id.sale_team_id:
                if r.sale_person_id.sale_team_id.user_id and r.sale_person_id.sale_team_id.user_id.partner_id.id not in r.message_follower_ids.ids:
                    subscribers += [r.sale_person_id.sale_team_id.user_id.partner_id.id]
                if r.sale_person_id.sale_team_id.regional_manager_id and r.sale_person_id.sale_team_id.regional_manager_id.partner_id.id not in r.message_follower_ids.ids:
                    subscribers += [r.sale_person_id.sale_team_id.regional_manager_id.partner_id.id]
            if subscribers:
                r.message_subscribe(subscribers)

    def action_confirm(self):
        super(PersonalSalesTarget, self).action_confirm()
        self.subscribe_approvers()

    def action_approve(self):
        if not self.env.user.has_group('to_sales_team_advanced.group_sale_team_leader'):
            raise ValidationError(_("You must be a sales team leader to approve personal sales targets for your team members"))
        super(PersonalSalesTarget, self).action_approve()

    @api.model_create_multi
    def create(self, vals_list):
        records = super(PersonalSalesTarget, self).create(vals_list)
        records.subscribe_salesperson()
        return records

    def write(self, vals):
        if 'sale_person_id' in vals:
            for r in self:
                r.message_unsubscribe([r.sale_person_id.partner_id.id])
        res = super(PersonalSalesTarget, self).write(vals)
        if 'sale_person_id' in vals:
            self.subscribe_salesperson()
        return res

    def _build_name(self):
        return "%s [%s] [%s ~ %s]" % (self.sale_person_id.name, self.target, format_date(self.env, self.start_date), format_date(self.env, self.end_date))

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
            domain = ['|', ('sale_person_id.name', 'ilike', name + '%'), ('name', operator, name)]
        tags = self.search(domain + args, limit=limit)
        return tags.name_get()
