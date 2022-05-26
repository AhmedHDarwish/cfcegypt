# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
class AccountJournal(models.Model):
    _inherit = "account.journal"

    note_payable_id = fields.Many2one('account.account')
    note_payable_under_deduct_id = fields.Many2one('account.account')
    note_recievable_id = fields.Many2one('account.account')
    cheque_under_collection_id = fields.Many2one('account.account')
    returned_cheques_id = fields.Many2one('account.account')
    cheque_books_ids = fields.One2many('cheque_system.cheque_book', 'journal_id', string='Cheque Books')
    
class ChequeBook(models.Model):
    _name = "cheque_system.cheque_book"
    _rec_name = "cheque_name"
    journal_id = fields.Many2one('account.journal')
    cheque_name = fields.Char(required = True)
    starting_number = fields.Integer(string = 'From',required = True)
    ending_number = fields.Integer(string = 'To',required = True)
    next_number = fields.Integer(string = 'Next Number',readonly = True,compute = '_compute_next_number')
    related_cheques_ids = fields.Many2many('cheque_system.cheque_payment')
    status = fields.Selection(selection = [('new','New'),('in_use','In Use'),('used','Used')],default = 'new',required = True)
    
    @api.depends('related_cheques_ids')
    def _compute_next_number(self):
        for rec in self:
            rec.next_number = rec.starting_number + len(rec.related_cheques_ids)
    
    @api.constrains('status')
    def check_status(self):
        for rec in self:
            is_all_cheques_used = len(rec.related_cheques_ids) == (rec.ending_number - rec.starting_number)
            if (rec.status == 'used' and not(is_all_cheques_used)) or (rec.status != 'used' and  is_all_cheques_used):
                raise UserError('You cant set status to this value')
                
            
                