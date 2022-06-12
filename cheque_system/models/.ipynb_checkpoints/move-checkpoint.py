# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
class AccountMove(models.Model):
    _inherit = "account.move"

    cheque_id = fields.Many2one('cheque_system.cheque_payment')
                
            
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    cheque_id = fields.Many2one('cheque_system.cheque_payment')