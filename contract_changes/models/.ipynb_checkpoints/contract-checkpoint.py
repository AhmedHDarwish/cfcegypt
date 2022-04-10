# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrContract(models.Model):
    _inherit = 'hr.contract'
    transportaion = fields.Monetary()
    other_allowances = fields.Monetary()
        
