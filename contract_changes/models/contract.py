# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrContract(models.Model):
    _inherit = 'hr.contract'
    transportation_type = fields.Selection(selection = [('cash','Cash'),('company_car','Company Car'),('company_bus','Company Bus')])
    transportaion_amount = fields.Monetary()
    housing_type = fields.Selection(selection = [('cash','Cash'),('single_house','Single House'),('shared_house','Shared House')])
    housing_amount = fields.Monetary()
    #medical
    has_medical_insurance = fields.Boolean()
    medical_class = fields.Selection(selection = [('a','A'),('b','B'),('c','C')])
    monthly_fees = fields.Monetary()
    medical_type = fields.Selection(selection = [('employee_pay','Employee Pay'),('company_pay','Company Pay'),('employee_pay_perc','Employee Pay %')])
    medical_percentage = fields.Float()
    medical_attachment = fields.Binary()
    #social
    has_social_insurance = fields.Boolean()
    social_isurance_number = fields.Char()
    social_isurance_date = fields.Date()
    social_isurance_attachment = fields.Binary()
    #allowances
    allowance_1 = fields.Monetary()
    allowance_2 = fields.Monetary()
    allowance_3 = fields.Monetary()
    allowance_4 = fields.Monetary()
    
    
    
