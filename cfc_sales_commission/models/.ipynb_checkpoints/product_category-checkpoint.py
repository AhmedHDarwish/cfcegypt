# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class ProductCategory(models.Model):
    _inherit = 'product.category'

    team_lead_eighty_percent = fields.Float(string="Team Leader Percentage 80%", digits=(12,6), default=0.000005)
    sale_person_eighty_percent = fields.Float(string="Sale Person Percentage 80%", digits=(12,6), default=0.000005)

    team_lead_hundred_percent = fields.Float(string="Team Leader Percentage 100%", digits=(12,6), default=0.000005)
    sale_person_hundred_percent = fields.Float(string="Sale Person Percentage 100%", digits=(12,6), default=0.000005)