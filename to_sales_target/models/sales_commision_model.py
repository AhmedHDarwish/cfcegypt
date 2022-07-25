# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleCommisionModel(models.Model):
    _name = 'sh.sale.commision.model'
    _description = 'Sales Commission Model'
    _rec_name = 'type'

    type = fields.Selection([('commission','Commission'),('deduction','Deduction')],string='Type')
    invoice_ref = fields.Many2one('account.move',string='Name')
    partner_id = fields.Many2one('res.partner','Customer')
    invoice_date = fields.Date('Invoice Date')
    source_document = fields.Char('Source Document')
    team_id = fields.Many2one('crm.team','Sales Team')
    team_leader = fields.Many2one('res.users','Team Leader')
    user_id = fields.Many2one('res.users','Salesperson')
    company_id = fields.Many2one('res.company','Company')
    due_date = fields.Date('Due Date')
    saleperson_eighty_commission_amount = fields.Float('Person Commission')
    saleperson_eighty_percentage = fields.Float('Sales Person %', digits=(12,6))
    saleperson_hundred_commission_amount = fields.Float('Person Commission')
    saleperson_hundred_percentage = fields.Float('Sales Person %', digits=(12,6))
    leder_eighty_commission_amount = fields.Float('Leader Commission')
    leader_eighty_percentage = fields.Float('Leader %', digits=(12,6))
    leder_hundred_commission_amount = fields.Float('Leader Commission')
    leader_hundred_percentage = fields.Float('Leader %', digits=(12,6))
    deduction_amount = fields.Float('Deduction')
    invoice_total = fields.Float('Total')
    payment_amount = fields.Float('Payment Amount')
    payment_date = fields.Date('Payment Date')
    