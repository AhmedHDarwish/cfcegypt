# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    sh_team_leader_id = fields.Many2one('res.users',string='Team Leader')
    sh_sales_person_ids = fields.Many2many('res.users',string='Salespersons',compute='_compute_sh_sales_person_ids')

    def add_to_list(self, current_user,add_user,  user_list):
        user_list.append(add_user.id)
        current_user.sh_sales_person_ids = [(6,0,user_list)]
        if add_user.sh_team_leader_id:
            current_user.add_to_list(current_user, add_user.sh_team_leader_id ,user_list)
        return user_list

    def _compute_sh_sales_person_ids(self):
        if self:
            for rec in self:
                rec.sh_sales_person_ids = False
                user_list = []
                user_list.append(rec.id)
                if rec.sh_team_leader_id:
                    rec.add_to_list(rec, rec.sh_team_leader_id, user_list)
                else:
                    rec.sh_sales_person_ids = [(6,0,user_list)]
