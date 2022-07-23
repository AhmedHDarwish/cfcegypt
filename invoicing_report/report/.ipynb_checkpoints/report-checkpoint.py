from odoo import models
from odoo.exceptions import ValidationError
from datetime import datetime
class PartnerXlsx(models.AbstractModel):
    _name = 'report.invoicing_reprot'
    _inherit = 'report.report_xlsx.partner_xlsx'
    
    def set_columns(self,sheet):
        sheet.set_column('A:N', 13)


    def just_change_color(self,base_format,color):
        base_format['bg_color'] = color
        return base_format
    def get_colors(self):
        return {
            'grey':'#cccccc',
            'light_green':'#93c47d',
        }

    def get_formats_dict(self,workbook):
        formats = {}
        border = 2
        normal_font_size = 10
        colors = self.get_colors()
        bold_format = {
            'border':border,
            'bold':True,
            'font_size':normal_font_size,
            'align':'vcenter',
            'text_wrap': True
        }
        normal_format = {
            'border':border,
            'bold':False,
            'font_size':normal_font_size,
            'align':'vcenter',
            'text_wrap': True
        }

        formats['normal_format'] = workbook.add_format(normal_format)
        formats['bold_format_green'] = workbook.add_format(self.just_change_color(bold_format,colors['light_green']))
        formats['bold_format_grey'] = workbook.add_format(self.just_change_color(bold_format,colors['grey']))
        
        formats['normal_format'].set_align('center')
        formats['bold_format_green'].set_align('center')
        formats['bold_format_grey'].set_align('center')
        
        return formats
    def set_sheet_1_headers(self,sheet_1,formats):
        sheet_1.write('A1', 'Sales Team',formats['bold_format_green'])
        sheet_1.write('B1', 'Sales Person',formats['bold_format_green'])
        sheet_1.write('C1', 'Customer',formats['bold_format_green'])
        sheet_1.write('D1', 'Product Cetgory',formats['bold_format_green'])
        sheet_1.write('E1', 'Product',formats['bold_format_green'])
        sheet_1.write('F1', 'Sales Number',formats['bold_format_green'])
        sheet_1.write('G1', 'Invoice Number',formats['bold_format_green'])
        sheet_1.write('H1', 'Invoice Date',formats['bold_format_green'])
        sheet_1.write('I1', 'Order Qty',formats['bold_format_green'])
        sheet_1.write('J1', 'Delivery Qty',formats['bold_format_green'])
        sheet_1.write('K1', 'Total Delivery Qty',formats['bold_format_green'])
        sheet_1.write('L1', 'Invoice Value',formats['bold_format_green'])
        sheet_1.write('M1', 'Unit Price',formats['bold_format_green'])
        if self.can_see_cost_analysis():
            sheet_1.write('N1', 'Unit Cost',formats['bold_format_green'])
            sheet_1.write('O1', 'Unit Margin',formats['bold_format_green'])
            sheet_1.write('P1', 'Total Cost',formats['bold_format_green'])
            sheet_1.write('Q1', 'Total Margin',formats['bold_format_green'])
        return 2
        

        
    def can_see_cost_analysis(self):
        return self.env.user.has_group('invoicing_report.group_can_see_cost_analysis')
    def write_normal_line(self,sheet,row,formats,line = None): 
        """
        line : account.move.line
        """
        date = datetime.strftime(line.move_id.invoice_date, "%Y-%m-%d")
        sheet.write(row,0,line.move_id.team_id.name,formats['normal_format'])
        sheet.write(row,1,line.move_id.invoice_user_id.name,formats['normal_format'])
        sheet.write(row,2,line.move_id.partner_id.name,formats['normal_format'])
        sheet.write(row,3,line.product_id.categ_id.name,formats['normal_format'])
        sheet.write(row,4,line.product_id.name,formats['normal_format'])
        sheet.write(row,5,line.get_so_name(),formats['normal_format'])
        sheet.write(row,6,line.move_id.name,formats['normal_format'])
        sheet.write(row,7,date,formats['normal_format'])
        sheet.write(row,8,line.get_order_qty(),formats['normal_format'])
        sheet.write(row,9,line.quantity,formats['normal_format'])
        sheet.write(row,10,line.get_delivery_qty(),formats['normal_format'])
        sheet.write(row,11,line.get_value_without_tax(),formats['normal_format'])
        sheet.write(row,12,line.convert_to_egp(line.price_unit),formats['normal_format'])
        if self.can_see_cost_analysis():
            cost = line.product_id.standard_price or line.product_id.lst_price
            sheet.write(row,13,cost,formats['normal_format'])
            sheet.write(row,14,line.get_margin(),formats['normal_format'])
            sheet.write(row,15,line.get_total_cost(),formats['normal_format'])
            sheet.write(row,16,line.get_total_margin(),formats['normal_format'])
        
    
    def write_totals_line(self,sheet,row,formats,totals_dict = {}):
        if totals_dict:
            sheet.merge_range(f'A{row + 1}:H{row + 1}', totals_dict['name'],formats['bold_format_grey'])
            sheet.write(row,8,totals_dict['order_qty'],formats['bold_format_grey'])
            sheet.write(row,9,totals_dict['delivery_qty'],formats['bold_format_grey'])
            sheet.write(row,10,totals_dict['delivery_total_qty'],formats['bold_format_grey'])
            sheet.write(row,11,totals_dict['invoice_value'],formats['bold_format_grey'])
            sheet.write(row,12,totals_dict['unit_price'],formats['bold_format_grey'])
            if self.can_see_cost_analysis():
                sheet.write(row,13,totals_dict['cost'],formats['bold_format_grey'])
                sheet.write(row,14,totals_dict['margin'],formats['bold_format_grey'])
                sheet.write(row,15,totals_dict['total_cost'],formats['bold_format_grey'])
                sheet.write(row,16,totals_dict['total_margin'],formats['bold_format_grey'])
    def write_all_lines(self,sheet,lines,formats,row_start = 1):
        """
        lines : [{
            'is_normal' : True or False
            'line' : account_move_line if is_normal else False,
            'totals':{
                'name' : '...',
                ...totals
            } if not(is_normal) else False
        }]
        """
        for line in lines:
            if line.get('is_normal',False):
                self.write_normal_line(sheet,row_start,formats,line['line'])
            else:
                self.write_totals_line(sheet,row_start,formats,line['totals'])
            row_start += 1
        return row_start
     
    
    def get_totals_dict(self,name,lines):
        if len(lines) == 0:
            return False
        totals = {'name' : name}
        totals.update(lines[0].get_totals(lines))
        return totals
    
    def change_in_group(self,currents,currents_lines,sheet_lines):
        """
        as each one change it's children's totals should be printed before it's
        so current and thier lines are passed cateory -> customer -> sales person -> sales team
        note : all arguments are pass by refrence
        """
        for i in range(0,len(currents)):
            current = currents[i]
            current_lines = currents_lines[i]
            sheet_lines.append({
                    'is_normal' : False,
                    'line' : False,
                    'totals' : self.get_totals_dict(f'{current.name} total',current_lines)
                })
            current_lines.clear()
        
    def generate_lines(self,records):
        lines = []
        current_sales_team_id = records[0].move_id.team_id
        current_sales_person = records[0].move_id.invoice_user_id
        current_customer = records[0].move_id.partner_id
        current_product_categ = records[0].product_id.categ_id
        sales_team_lines = []
        sales_person_lines = []
        customer_lines = []
        categ_lines = []
        for rec in records:
            
            if rec.move_id.team_id.id != current_sales_team_id.id:
                currents = [current_product_categ,current_customer,current_sales_person,current_sales_team_id]
                currents_lines = [categ_lines,customer_lines,sales_person_lines,sales_team_lines]
                self.change_in_group(currents,currents_lines,lines)
                current_sales_team_id = rec.move_id.team_id
                current_sales_person = rec.move_id.invoice_user_id
                current_customer = rec.move_id.partner_id
                current_product_categ = rec.product_id.categ_id
            elif rec.move_id.invoice_user_id.id != current_sales_person.id:
                currents = [current_product_categ,current_customer,current_sales_person]
                currents_lines = [categ_lines,customer_lines,sales_person_lines]
                self.change_in_group(currents,currents_lines,lines)
                current_sales_person = rec.move_id.invoice_user_id
                current_customer = rec.move_id.partner_id
                current_product_categ = rec.product_id.categ_id
            elif rec.move_id.partner_id.id != current_customer.id:
                currents = [current_product_categ,current_customer]
                currents_lines = [categ_lines,customer_lines]
                self.change_in_group(currents,currents_lines,lines)
                current_customer = rec.move_id.partner_id
                current_product_categ = rec.product_id.categ_id
            elif rec.product_id.categ_id.id != current_product_categ.id:
                currents = [current_product_categ]
                currents_lines = [categ_lines]
                self.change_in_group(currents,currents_lines,lines)
                current_product_categ = rec.product_id.categ_id
                
            sales_team_lines.append(rec)
            sales_person_lines.append(rec)
            customer_lines.append(rec)
            categ_lines.append(rec)
            lines.append({
                'is_normal' : True,
                'line' : rec,
                'totals' : False
            })
        # last sales team
        currents = [current_product_categ,current_customer,current_sales_person,current_sales_team_id]
        currents_lines = [categ_lines,customer_lines,sales_person_lines,sales_team_lines]
        self.change_in_group(currents,currents_lines,lines)
        # footer
        lines.append({
            'is_normal' : False,
            'line' : False,
            'totals' : self.get_totals_dict('Grand Total',records)
        })
        return lines
    def generate_xlsx_report(self, workbook, data, partners):
        sheet_1 = workbook.add_worksheet('Invoicing report')
        formats = self.get_formats_dict(workbook)
        self.set_columns(sheet_1)
        row_after_header = self.set_sheet_1_headers(sheet_1,formats) 
        lines = self.generate_lines(partners)
        footer_row = self.write_all_lines(sheet_1,lines,formats)
