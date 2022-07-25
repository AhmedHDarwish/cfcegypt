from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CRMTeamRegion(models.Model):
    _name = 'crm.team.region'
    _inherit = 'mail.thread'
    _description = 'Sales Region'

    name = fields.Char(string='Name', required=True, index=True)
    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one('res.users', string='Manager', help="The one who manager sales in this region")
    team_ids = fields.One2many('crm.team', 'crm_team_region_id', string="Teams / Channels")
    member_ids = fields.Many2many('res.users', string='Sales Persons', compute='_compute_member_ids', store=True)
    parent_id = fields.Many2one('crm.team.region', string="Parent Region", ondelete='cascade', help="The parent region to which this region belongs.")
    child_ids = fields.One2many('crm.team.region', 'parent_id', string="Child Regions")
    recursive_child_ids = fields.Many2many('crm.team.region', 'sale_team_region_recursive_children_rel', 'parent_id', 'child_id', string="Recursive Children",
                                           compute='_compute_recursive_child_ids', store=True, help="The recursive children of this sales region.")
    recursive_parent_ids = fields.Many2many('crm.team.region', 'sale_team_region_recursive_children_rel', 'child_id', 'parent_id', string="Recursive Parent", readonly=True)

    recursive_user_ids = fields.Many2many('res.users', 'sale_team_region_recursive_manager_rel', 'region_id', 'user_id', string="Recursive Managers",
                                           compute='_compute_recursive_user_ids', store=True,
                                           help="The recursive managers of this sales region.")

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive region.'))
        return True

    def _get_children(self):
        self._check_category_recursion()
        child_ids = self.mapped('child_ids')
        for child_id in child_ids:
            child_ids += child_id._get_children()
        return child_ids

    @api.depends('child_ids', 'child_ids.recursive_child_ids')
    def _compute_recursive_child_ids(self):
        for r in self:
            r.recursive_child_ids = r._get_children()

    @api.depends('recursive_parent_ids', 'user_id', 'parent_id.recursive_user_ids')
    def _compute_recursive_user_ids(self):
        for r in self:
            recursive_user_ids = r.user_id
            recursive_user_ids |= r.recursive_parent_ids.mapped('user_id')
            r.recursive_user_ids = recursive_user_ids

    @api.depends('team_ids', 'team_ids.member_ids')
    def _compute_member_ids(self):
        for r in self:
            member_ids = r.team_ids.mapped('member_ids')
            member_ids |= r.team_ids.mapped('user_id')
            r.member_ids = member_ids and member_ids.ids or []
