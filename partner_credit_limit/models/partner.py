# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    over_credit = fields.Boolean('Allow Over Credit?')
    over_credit_days = fields.Boolean('Allow Over Credit Days?')
    credit_days = fields.Char('Credit Days')
