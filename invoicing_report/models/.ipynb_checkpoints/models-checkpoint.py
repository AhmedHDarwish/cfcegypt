from odoo import models, fields, api
from odoo.exceptions import Warning, UserError, ValidationError

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    

    def round_float(self,amount):
        return float("{:.2f}".format(amount))
    def get_cost(self,product):
        return product.standard_price or product.lst_price
    def get_totals(self,lines):
        totals = {}
        for line in lines:
            totals['order_qty'] = totals.get('order_qty',0) + line.get_order_qty() 
            totals['delivery_qty'] = totals.get('delivery_qty',0) + line.get_delivery_qty() 
            totals['invoice_value'] = totals.get('invoice_value',0) + line.get_value_without_tax()
            totals['unit_price'] = totals.get('unit_price',0) + line.price_unit
            cost = self.get_cost(line.product_id)
            totals['cost'] = totals.get('cost',0) + cost
            totals['margin'] = totals.get('margin',0) + line.get_margin()
            totals['total_cost'] = totals.get('total_cost',0) + line.get_total_cost()
            totals['total_margin'] = totals.get('total_margin',0) + line.get_total_margin()
        return totals
    def get_related_so_lines(self):
        return self.sale_line_ids
    def get_margin(self):
        return self.round_float(self.price_unit - self.product_id.standard_price)
    def get_total_cost(self):
        cost = self.get_cost(self.product_id)
        return self.round_float(self.get_order_qty() * cost)
    def get_total_margin(self):
        return self.round_float(self.price_subtotal - self.get_total_cost())
    
    def get_order_qty(self):
        lines = self.get_related_so_lines()
        if len(lines) > 0:
            return self.round_float(sum([line.product_uom_qty for line in lines]))
        return 0
    
    def get_delivery_qty(self):
        lines = self.get_related_so_lines()
        if len(lines) > 0: 
            return self.round_float(sum([line.qty_delivered for line in lines]))
        return 0
    def get_so_name(self):
        return self.sale_line_ids[0].order_id.name if len(self.sale_line_ids) > 0 else ''
    def get_value_without_tax(self):
        return self.round_float(self.price_unit * self.quantity)
        

        