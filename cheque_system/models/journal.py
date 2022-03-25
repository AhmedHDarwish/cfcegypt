# -*- coding: utf-8 -*-

from odoo import api, fields, models

class AccountJournal(models.Model):
    _inherit = "account.journal"

    note_payable_id = fields.Many2one('account.account')
    note_payable_under_deduct_id = fields.Many2one('account.account')
    note_recievable_id = fields.Many2one('account.account')
    cheque_under_collection_id = fields.Many2one('account.account')
    returned_cheques_id = fields.Many2one('account.account')