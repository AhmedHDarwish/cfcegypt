# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class ChequePayment(models.Model):
    _name = "cheque_system.cheque_payment"
    currency_id = fields.Many2one('res.currency', string='Currency')
    name = fields.Char(required=1)
    amount = fields.Monetary(currency_field='currency_id',required=1)
    type = fields.Selection([
        ('outbound', 'Send'),
        ('inbound', 'Receive'),
    ], string='Payment Type', default='inbound', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner',required=1)
    date = fields.Date(required=1)
    ref = fields.Char('Beneficiary')
    journal_id = fields.Many2one('account.journal',domain = "[('type','=','bank')]",required=1)
    company_id = fields.Many2one('res.company',string='company',default=lambda self: self.env.company)
    to_be_posted_account_move_id = fields.Many2one('account.move')
    #state
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string="State", default='draft',compute = '_compute_state',copy = False) #this field for ui purposes
    @api.depends('outbound_status','inbound_status','type')
    def _compute_state(self):
        for rec in self:
            state = rec.outbound_status if rec.type == 'outbound' else rec.inbound_status
            rec.state = 'draft' if state == 'new' else 'confirm'
    #open buttons
    def open_journal_entry(self):
        [action] = self.env.ref(
            'cheque_system.cheque_action_move_journal_line').read()
        ids = self.env['account.move'].search([('cheque_id', '=', self.id)])
        id_list = []
        for cheque_id in ids:
            id_list.append(cheque_id.id)
        action['domain'] = [('id', 'in', id_list)]
        return action
    #utilties
    def check_payment_amount(self):
        if self.amount <= 0.0:
            raise UserError("Amount must be greater than zero!")
    def get_partner_id_for_entry_lines(self,account):
        return self.partner_id.id
    def get_move_line(self, account,field_name):
        return {
            'cheque_id': self.id,
            'partner_id': self.get_partner_id_for_entry_lines(account),
            'account_id': account,
            field_name: self.amount,
            'ref': self.ref,
            'date': fields.Date.today(),
            'date_maturity': self.due_date,
        }
    def get_move_vals(self, debit_line, credit_line):
        return {
            'cheque_id': self.id,
            'date': fields.Date.today(),
            'journal_id': self.journal_id.id,
            'partner_id': self.partner_id.id,
            'ref': self.ref,
            'line_ids': [(0, 0, debit_line),
                         (0, 0, credit_line)]
        }
    def create_account_move(self,debit_account,credit_account):
        move = self.env['account.move']

        self.check_payment_amount()  # amount must be positive

        move_line_vals_debit = self.get_move_line(debit_account,'debit')
        move_line_vals_credit = self.get_move_line(credit_account,'credit')

        #create move and post it
        move_vals = self.get_move_vals(
            move_line_vals_debit, move_line_vals_credit)
        move_id = move.create(move_vals)
        return move_id
    #outbound logic
    cheque_book_id = fields.Many2one('cheque_system.cheque_book')
    cheque_number = fields.Char(readonly = True,compute = '_get_cheque_number',store = True)
    
    @api.depends('cheque_book_id')
    def _get_cheque_number(self):
        for rec in self:
            if rec.state != 'confirm':
                rec.cheque_number = rec.cheque_book_id.next_number
    due_date = fields.Date()
    outbound_status = fields.Selection([
        ('new', 'New'),
        ('issued', 'Issued'),
        ('handed', 'Handed'),
        ('rejected', 'Rejected'),
        ('under_deduct', 'Under Deduct'),
        ('done', 'Done'),
       
    ], string='Status', default='new', required=True, readonly=True,copy = False)  
    def post_entries(self):
        outgoing_cheques_to_be_posted = self.env['cheque_system.cheque_payment'].search([('type','=','outbound'),('outbound_status','in',('issued','handed')),('due_date','<=',fields.Date().today())])
        for cheque in outgoing_cheques_to_be_posted:
            if cheque.to_be_posted_account_move_id.state == 'draft':
                cheque.to_be_posted_account_move_id.action_post()
            cheque.outbound_status = 'under_deduct'
        incoming_cheques_to_be_posted = self.env['cheque_system.cheque_payment'].search([('type','=','inbound'),('inbound_status','not in',('new','cancel')),('due_date','<=',fields.Date().today())])
        for cheque in incoming_cheques_to_be_posted:
            if cheque.to_be_posted_account_move_id.state == 'draft':
                cheque.to_be_posted_account_move_id.action_post()
    def outbound_post(self):
        posted_move_id = self.create_account_move(debit_account = self.partner_id.property_account_payable_id.id,credit_account = self.journal_id.note_payable_id.id)
        posted_move_id.action_post()
        to_be_posted_move_id = self.create_account_move(debit_account = self.journal_id.note_payable_id.id,credit_account = self.journal_id.note_payable_under_deduct_id.id)
        to_be_posted_move_id.date = self.due_date
        self.to_be_posted_account_move_id = to_be_posted_move_id.id
        self.cheque_book_id.related_cheques_ids = [(4,self.id)]
        self.outbound_status = 'issued'
    def delivered(self):
        self.outbound_status = 'handed'
    def outbound_done(self):
        posted_move_id = self.create_account_move(debit_account = self.journal_id.note_payable_under_deduct_id.id,credit_account = self.journal_id.default_account_id.id)
        posted_move_id.action_post()
        self.outbound_status = 'done'
    def outbound_return(self):
        posted_move_id = self.create_account_move(debit_account = self.journal_id.note_payable_under_deduct_id.id,credit_account = self.partner_id.property_account_payable_id.id)
        posted_move_id.action_post()
        self.outbound_status = 'rejected'
    #inbound logic
    inbound_cheque_number = fields.Char(string = 'Cheque Number')
    bank_id = fields.Many2one('res.bank')
    inbound_status = fields.Selection([
        ('new', 'New'),
        ('handed', 'Handed'),
        ('paid', 'Paid'),
        ('under_collection', 'Under Collection'),
        ('rejected', 'Rejected'),
        ('re_under_collection', 'Re Under Collection'),
        ('replacment', 'Replacmnet'),
        ('cancel', 'Cancel'),
    ], string='Status', default='new', required=True, readonly=True,copy = False)  

    def inbound_post(self):
        posted_move_id = self.create_account_move(debit_account = self.journal_id.note_recievable_id.id,credit_account = self.partner_id.property_account_receivable_id.id)
        posted_move_id.action_post()
        to_be_posted_move_id = self.create_account_move(debit_account = self.journal_id.cheque_under_collection_id.id,credit_account = self.journal_id.note_recievable_id.id)
        to_be_posted_move_id.date = self.due_date
        self.to_be_posted_account_move_id = to_be_posted_move_id.id
        self.inbound_status = 'handed'
    def inbound_validate(self):
        posted_move_id = self.create_account_move(debit_account = self.journal_id.default_account_id.id,credit_account = self.journal_id.cheque_under_collection_id.id)
        posted_move_id.action_post()
        self.inbound_status = 'paid'
                
    def inbound_reject(self):
        posted_move_id = self.create_account_move(debit_account = self.partner_id.property_account_receivable_id.id,credit_account = self.journal_id.cheque_under_collection_id.id)
        posted_move_id.action_post()
        self.inbound_status = 'rejected'    
    def inbound_recollect(self):
        posted_move_id = self.create_account_move(debit_account = self.journal_id.cheque_under_collection_id.id,credit_account = self.journal_id.returned_cheques_id.id)
        posted_move_id.action_post()
        self.inbound_status = 're_under_collection'      
    def inbound_replace(self):
        posted_move_id = self.create_account_move(debit_account = self.journal_id.default_account_id.id,credit_account = self.journal_id.cheque_under_collection_id.id)
        posted_move_id.action_post()
        self.inbound_status = 'replacment'  
    def inbound_cancel(self):
        posted_move_id = self.create_account_move(debit_account = self.partner_id.property_account_receivable_id.id,credit_account = self.journal_id.cheque_under_collection_id.id)
        posted_move_id.action_post()
        self.inbound_status = 'cancel'  