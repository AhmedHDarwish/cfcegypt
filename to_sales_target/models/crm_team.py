from odoo import fields, models, api

class CrmTeam(models.Model):
    _name = 'crm.team'
    _inherit = ['crm.team', 'sales.target.mixin']

    team_sales_target_ids = fields.One2many('team.sales.target', 'crm_team_id', string='Sales Targets')

    approved_targets_count = fields.Integer(string='Sales Targets Count', compute='_compute_approved_targets_count', store=True)

    @api.depends('team_sales_target_ids', 'team_sales_target_ids.state')
    def _compute_approved_targets_count(self):
        for r in self:
            r.approved_targets_count = len(r.team_sales_target_ids.filtered(lambda t: t.state == 'approved'))

    def get_target_by_period(self, start_date, end_date, state='approved'):
        self.ensure_one()
        matched_target_ids = self.team_sales_target_ids.filtered(lambda target: target.end_date >= start_date \
                                                                 and target.start_date <= end_date \
                                                                 and target.state == state)
        target = matched_target_ids.get_target_sum(start_date, end_date)
        return target, matched_target_ids

