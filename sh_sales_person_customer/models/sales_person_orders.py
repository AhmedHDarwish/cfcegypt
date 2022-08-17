# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    sales_persons_ids = fields.Many2many("res.users", string="Allocate Sales Persons",compute='_compute_sales_persons_ids',store=True)

    @api.depends('user_id')
    def _compute_sales_persons_ids(self):
        if self:
            for rec in self:
                rec.sales_persons_ids = False
                if rec.user_id and rec.user_id.sh_sales_person_ids:
                    rec.sales_persons_ids = [(6,0,rec.user_id.sh_sales_person_ids.ids)]
        
    # To apply domain to customer search
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        search_domain = [('name', operator, name)]
        if self.env.user.has_group('sales_team.group_sale_salesman') and not(self.env.user.has_group('sales_team.group_sale_salesman_all_leads')):
            search_domain=['|','|', ('sales_persons_ids', 'in', self.env.user.id),('user_id', '=', self.env.user.id),('id', '=', self.env.user.partner_id.id)]
        partners = self.search(search_domain)
        return partners.name_get()
    
    # To apply domain to menu action
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self.env.user.has_group('sales_team.group_sale_salesman') and not(self.env.user.has_group('sales_team.group_sale_salesman_all_leads')):
            args = args + ['|','|',('sales_persons_ids', 'in', self.env.user.id),('user_id', '=', self.env.user.id),('id', '=', self.env.user.partner_id.id)]
        return super(ResPartner, self).search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
        )
        
    @api.model
    def default_get(self, fields):
        vals = super(ResPartner, self).default_get(fields)
        if self.env.user:
            vals.update({
                'user_id': self.env.user.id,
            })
        return vals        
    