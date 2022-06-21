from odoo import fields, models


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    crm_team_region_id = fields.Many2one('crm.team.region', string='Region', help='The region to which this sales team belongs')

    regional_manager_id = fields.Many2one('res.users', string='Regional Manager',
                                          related='crm_team_region_id.user_id', store=True, readonly=True,
                                          help="The one who has the rights to approve sales targets"
                                          " for the team and the team members")