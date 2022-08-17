# See LICENSE file for full copyright and licensing details.

from odoo import fields, models,api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    credit_limit_actual = fields.Float()
    @api.onchange('credit_limit_actual')
    def set_credit_limit(self):
        self.credit_limit = self.credit_limit_actual
    over_credit = fields.Boolean('Allow Over Credit?')
    over_credit_days = fields.Boolean('Allow Over Credit Days?')
    credit_days = fields.Char('Credit Days')
