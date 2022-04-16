# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    def calculate_tax(self,amount):
        tax_slides = self.env['tax_slide.tax_slide'].search([],order='priority asc')
        if len(tax_slides) == 0:
            return 0
        for i in range(len(tax_slides)):
            current_slide = tax_slides[i]
            if current_slide.max_salary >= amount:
                return current_slide.calculate_tax(amount)
            if i + 1 >= len(tax_slides):
                return current_slide.calculate_tax(amount)
        
