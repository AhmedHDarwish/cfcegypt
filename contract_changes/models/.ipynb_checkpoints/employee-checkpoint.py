# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    has_social_insurance = fields.Boolean()
    social_insurance = fields.Char()
    has_medical_insurance = fields.Boolean()
    employee_pays = fields.Boolean('Employee pays?')
    medical_insurance = fields.Float()
        
