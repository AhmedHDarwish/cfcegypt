import math

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SalesTargetMixin(models.AbstractModel):
    _name = 'sales.target.mixin'
    _description = "Sales Target Mixin"

    def get_target_by_period(self, start_date, end_date, state='approved'):
        raise ValidationError(_("The method `%s` has not been implemented for the model '%s'") % self.name)

    def get_month_target(self, month, year):
        if month <= 0 or month > 12:
            raise ValidationError(_("Month must be 1~12. You've input %s") % (month,))
        month_start_date = datetime(year, month, 1).date()
        month_end_date = (datetime(year, month, 1) + relativedelta(months=1) + timedelta(days=-1)).date()

        return self.get_target_by_period(month_start_date, month_end_date)

    def get_week_target(self, week, year):
        if week <= 0 or week > 52:
            raise ValidationError(_("Week must be 1~52. You've input %s") % (week,))
        week_date = str(year) + ' ' + str(week)
        week_start_date = datetime.strptime(week_date + ' 1', "%Y %W %w").date()
        week_end_date = datetime.strptime(week_date + ' 0', "%Y %W %w").date()

        return self.get_target_by_period(week_start_date, week_end_date)

    def get_quarter_target(self, quarter, year):
        if quarter <= 0 or quarter > 4:
            raise ValidationError(_("Quarter must be 1~4. You've input %s") % (quarter,))
        quarter_start_date = datetime(year, 3 * quarter - 2, 1).date()
        quarter_end_date = (datetime(year, 3 * quarter, 1) + relativedelta(months=1) + timedelta(days=-1)).date()

        return self.get_target_by_period(quarter_start_date, quarter_end_date)

    def get_year_target(self, year):
        year_start_date = datetime(year, 1, 1).date()
        year_end_date = datetime(year, 12, 31).date()

        return self.get_target_by_period(year_start_date, year_end_date)

    def get_target_by_date(self, date, period='month'):
        date = fields.Date.from_string(date)
        if period == 'month':
            return self.get_month_target(date.month, date.year)
        elif period == 'week':
            week = date.isocalendar()[1]
            return self.get_week_target(week, date.year)
        elif period == 'quarter':
            quarter = math.ceil(date.month / 3)
            return self.get_quarter_target(quarter, date.year)
        elif period == 'year':
            return self.get_year_target(date.year)
        elif period == 'day':
            return self.get_target_by_period(date, date)

