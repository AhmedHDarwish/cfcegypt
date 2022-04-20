# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.exceptions import UserError, ValidationError

class Attendance(models.Model):
    _inherit = 'hr.attendance'
    
    def get_work_entry_type_id(self):
        work_entry_type_id = self.env['hr.work.entry.type'].search([('name','=','Actual Attendace')])
        if len(work_entry_type_id) == 0:
            work_entry_type_id = self.env['hr.work.entry.type'].create({
                'name' : 'Actual Attendace',
                'code' : 'WORK101'
            })
        else:
            work_entry_type_id = work_entry_type_id[0]
        return work_entry_type_id.id
    @api.model
    def create(self,vals):
        res = super().create(vals)
        work_entry_type_id = res.get_work_entry_type_id()
        self.env['hr.work.entry'].create({
            'name' : f'Actual Attendace : {res.employee_id.name}',
            'employee_id' : res.employee_id.id,
            'date_start' : res.check_in,
            'date_stop' : res.check_out,
            'work_entry_type_id' : work_entry_type_id,
            'state' : 'draft'
        })
        return res
        
