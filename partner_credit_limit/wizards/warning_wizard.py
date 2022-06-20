# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PartnerCreditLimitWarningWizard(models.TransientModel):
    _name = 'partner.credit.limit.warning.wizard'
    _description = 'Warning Message'
    
    msg = fields.Text('Message')
    sale_order_id = fields.Many2one('sale.order',string='oder')
    
    def allow_action_confirm(self):
        self.sale_order_id.with_context({'partner_credit_limit_from_wizard':True}).action_confirm()
        
    @api.model
    def default_get(self, fields):
        res = super(PartnerCreditLimitWarningWizard, self).default_get(fields)
        active_ids = self.env.context.get('active_ids')
        order = self.env['sale.order'].browse(active_ids)
        res.update({
            'sale_order_id':order.id,
            })
        return res
                
        
