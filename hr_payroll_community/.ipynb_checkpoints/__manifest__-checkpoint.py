# -*- coding: utf-8 -*-

{
    'name': 'Odoo13 Payroll',
    'category': 'Generic Modules/Human Resources',
    'version': '13.0.1.5.3',
    'author': 'Odoo SA,Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'summary': 'Manage your employee payroll records',
    'images': ['static/description/banner.gif'],
    'description': "Odoo 13 Payroll, Payroll, Odoo 13,Odoo Payroll, Odoo Community Payroll",
    'depends': [
        'hr_contract',
        'hr_holidays',
        'hr_contract_types',
        'hr_payroll'
    ],
    'data': [
#         'security/hr_payroll_security.xml',
        'security/ir.model.access.csv',
#         'wizard/hr_payroll_payslips_by_employees_views.xml',
        'views/hr_contract_views.xml',
#         'views/hr_salary_rule_views.xml',
#         'views/hr_payslip_views.xml',
#         'views/hr_employee_views.xml',
#         'data/hr_payroll_sequence.xml',
#         'views/hr_payroll_report.xml',
#         'wizard/hr_payroll_contribution_register_report_views.xml',
#         'views/res_config_settings_views.xml',
#         'views/report_contributionregister_templates.xml',
#         'views/report_payslip_templates.xml',
#         'views/report_payslipdetails_templates.xml',
    ],
    'license': 'AGPL-3',
    # 'demo': ['data/hr_payroll_demo.xml'],
}
