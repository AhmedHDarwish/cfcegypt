from odoo import fields, models, api


class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = ['res.users', 'sales.target.mixin']

    personal_sales_target_ids = fields.One2many('personal.sales.target', 'sale_person_id', string='Personal Sales Target')
    approved_targets_count = fields.Integer(string='Sales Targets Count', compute='_compute_approved_targets_count', store=True)

    @api.depends('personal_sales_target_ids', 'personal_sales_target_ids.state')
    def _compute_approved_targets_count(self):
        for r in self:
            r.approved_targets_count = len(r.personal_sales_target_ids.filtered(lambda t: t.state == 'approved'))

    def get_target_by_period(self, start_date, end_date, state='approved'):
        matched_target_ids = self.personal_sales_target_ids.filtered(lambda target: target.end_date >= start_date \
                                                                     and target.start_date <= end_date \
                                                                     and target.state == state)
        target = matched_target_ids.get_target_sum(start_date, end_date)
        return target, matched_target_ids
