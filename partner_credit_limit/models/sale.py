# See LICENSE file for full copyright and licensing details.


from odoo import api, models, fields, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_limit(self):
        values = {}
        self.ensure_one()
        partner = self.partner_id
        due_days = []
        user_id = self.env['res.users'].search([
            ('partner_id', '=', partner.id)], limit=1)
        if user_id and not user_id.has_group('base.group_portal') or not \
                user_id:
            moveline_obj = self.env['account.move.line']
            move_obj = self.env['account.move']
            movelines = moveline_obj.search(
                [('partner_id', '=', partner.id),
                 ('account_id.user_type_id.name', 'in',
                  ['Receivable', 'Payable'])]
            )
            days_movelines = move_obj.search(
                [
                    ('partner_id', '=', partner.id),
                    ('payment_state', '!=', 'paid'),
                ]
            )

            for rec in days_movelines:
                if rec.invoice_date_due:
                    due_days.append(rec.invoice_date_due)
            due_date = fields.Datetime.now().date()
            if due_days:
                due_date = min(due_days)

            now = fields.Datetime.now().date()
            days = due_date - now

            confirm_sale_order = self.search([('partner_id', '=', partner.id),
                                              ('state', '=', 'sale')])
            debit, credit = 0.0, 0.0
            amount_total = self.amount_total
            for status in confirm_sale_order:
                amount_total += status.amount_total
            for line in movelines:
                credit += line.credit
                debit += line.debit
            partner_credit_limit = (partner.credit_limit - debit) + credit
            available_credit_limit = \
                ((partner_credit_limit -
                  (amount_total - debit)) + self.amount_total)
            days_limit = int(partner.credit_days) < abs(days.days)

            check_limit = (amount_total - debit) > partner_credit_limit
            if (amount_total - debit) > partner_credit_limit:
                if not partner.over_credit:
                    values = {
                        'status': False,
                        'available_credit_limit': available_credit_limit,
                        'check_limit': check_limit,
                        'days_limit': days_limit,
                        'credit_days': int(partner.credit_days),
                        'due_days': days.days,
                    }
                    return values
                partner.write(
                    {'credit_limit': credit - debit + self.amount_total}
                )
            if days_limit:
                if not partner.over_credit_days:
                    values = {
                        'status': False,
                        'available_credit_limit': available_credit_limit,
                        'days_limit': days_limit,
                        'credit_days': int(partner.credit_days),
                        'due_days': days.days,
                    }
                    return values
            return {
                'status': True,
                'available_credit_limit': available_credit_limit,
                'days_limit': days_limit,
                'credit_days': int(partner.credit_days),
                'due_days': days.days,
            }

    def action_confirm(self):
        if self.env.context.get("partner_credit_limit_from_wizard", False):
            return super(SaleOrder, self).action_confirm()
        for order in self:
            values_dic = order.check_limit()
            status = values_dic.get('status')
            days_limit = values_dic.get('days_limit')
            due_days = values_dic.get('due_days')
            check_limit = values_dic.get('check_limit')
            credit_days = 0
            due_days = 0
            credit_days = values_dic.get('credit_days')
            if values_dic.get('credit_days'):
                credit_days = values_dic.get('credit_days')
            if values_dic.get('due_days'):
                due_days = values_dic.get('due_days')
            days = abs(credit_days) - abs(due_days)

            if not status:
                available_credit_limit = values_dic.get(
                    'available_credit_limit')

                message = ''
                message += 'You can not confirm Sale Order \n'
                if check_limit:
                    if not self.partner_id.over_credit:
                        message += 'Your available credit limit Amount = %s \n' % (
                            available_credit_limit)
                if days_limit:
                    if not self.partner_id.over_credit_days:
                        message += 'Your available credit days = %s Days\n' % (
                            days)
                message += 'check "%s" Accounts or credit limits.' % (
                    self.partner_id.name)

                message = message
                action = {
                    'name': _("Something went wrong!"),
                    'view_mode': 'form',
                    'view_type': 'form',
                    'res_model': 'partner.credit.limit.warning.wizard',
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': {
                            'default_msg': message,
                    },
                }
                return action
        return super(SaleOrder, self).action_confirm()

    @api.constrains('amount_total')
    def check_amount(self):
        for order in self:
            order.check_limit()
