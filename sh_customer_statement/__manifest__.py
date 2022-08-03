# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Customer Account Statement",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "13.0.4",
    "category": "Accounting",
    "summary": "Bank Statement, Accounts Statement, Customer Bank Statement, Client Statement, Contact Statement, Overdue Statement, Account Statement Report, Partner Statement of Account, Bank Account Detail Report, Bank Details Odoo",
    "description": """This module allows customers to see statements as well as overdue statement details. You can send statements by email to the customers. You can also see customers mail log history with statements and overdue statements. You can also send statements automatically weekly, monthly & daily using cron job. You can filter statements by dates, statements & overdue statements. You can group by statements by the statement type, mail sent status & customers. You can print statements and overdue statements.""",
    "depends": [
        'account',
        'sh_sales_person_customer'
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/mail_history.xml',
        'views/res_config_setting.xml',
        'views/res_partner.xml',
        'report/customer_statement_report.xml',
        'report/customer_due_statement_report.xml',
        'report/customer_filter_statement_report.xml',
        'report/paperformat.xml',
        'data/email_data.xml',
        'data/statement_cron.xml',
        'views/assets.xml',
        'views/customer_statement_portal_templates.xml',
        'wizard/customer_statement_report_wizard.xml',
        'report/salesperson_customer_statement_report.xml',
    ],
    "images": ["static/description/background.png", ],
    "license": "OPL-1",
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "50",
    "currency": "EUR"
}
