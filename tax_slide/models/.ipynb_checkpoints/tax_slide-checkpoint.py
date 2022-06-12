# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TaxSlide(models.Model):
    _name = 'tax_slide.tax_slide'

    name = fields.Char()
    priority = fields.Integer(required=True)
    max_salary = fields.Float(required=True)
    tax_slide_lines = fields.One2many('tax_slide.tax_slide_line', 'tax_slide_id', "Lines") 
    
    _sql_constraints = [('priority_unique', 
                      'unique(priority)',
                      'priority must be unique')]
    def calculate_tax(self,amount):
        rem = amount
        tax = 0
        for line in self.tax_slide_lines:
            if rem - line.amount <= 0 :
                tax += rem * (line.percentage / 100)
                return tax
            tax += line.tax_amount
            rem -= line.amount
        return tax
    
    @api.onchange('tax_slide_lines')
    def assure_amount_less_than_max_salary(self):
        lines_sum = sum([line.amount for line in self.tax_slide_lines])
        if lines_sum > self.max_salary:
            raise ValidationError('sum of amouts cannot exceed max salary')
        
    
class TaxSlide(models.Model):
    _name = 'tax_slide.tax_slide_line'
    tax_slide_id = fields.Many2one('tax_slide.tax_slide')
    
    amount = fields.Float(required=True)
    percentage = fields.Float(required=True)
    tax_amount = fields.Float(compute='compute_tax_amount')
    note = fields.Char()
    
    @api.depends('amount','percentage')
    def compute_tax_amount(self):
        for rec in self:
            rec.tax_amount = rec.amount * (rec.percentage / 100)