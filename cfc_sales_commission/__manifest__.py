{
    'name': "Cfc Sales Commission Test",
    'summary': """
Sales commission based on target reached.
""",
    'category': 'Sales',
    'version': '1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['product','account','to_sales_target','to_sales_target_sale'],

    # always loaded
    'data': [
        'views/product_category_views.xml',
        'views/account_move_views.xml',
        'views/view_invoice_commission_deduction_tree.xml',
        'views/team_sales_target_views.xml',
        'views/personal_sales_target_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
