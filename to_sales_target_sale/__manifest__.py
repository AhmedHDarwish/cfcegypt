{
    'name': "Sales Target Management - Sales Management",
    'name_vi_VN': "Quản lý mục tiêu doanh số - Quản lý bán hàng",
    'summary': """
Integrated Sales Target Management with Sales Application""",
    'summary_vi_VN': """
Tích hợp ứng dụng quản lý mục tiêu doanh số với ứng dụng bán hàng""",
    'description': """
This application integrates the Sales Target Management application and the Sales Management
to allow you to manage sales targets for sales persons and sales team in the Sales Management application

It also helps you get insight of sales performance against the targets with several Key Performance Indexes

Key Features
============
1. Sales Targets for sales persons in Sales Management application
    * Sales person submit their target
    * Sales Team Leader approves/refused/adjusts the target
2. Sales Targets for Sales Teams in Sales Management application
    * Team Leader register their team's sales target
    * Regional Sales Manager can either approve or refuse and request changes
3. Measure sales targets in reach automatically
    * For Individuals / Sales persons
        * Total Confirmed Sales in the period of the target
        * Sales Target Reach (in percentage, based on Confirmed Sales)
        * Total Sales that have been invoices in the period of the target
        * Invoiced Target Reach (in percentage, based on Invoiced Sales)
    * For A Sales Team
        * Total Confirmed Sales in the period of the target
        * Sales Target Reach (in percentage, based on Confirmed Sales)
        * Total Sales that have been invoices in the period of the target
        * Invoiced Target Reach (in percentage, based on Invoiced Sales)
        
Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,
    'description_vi_VN': """
Module này làm gì
=================
Ứng dụng này tích hợp ứng dụng Quản lý mục tiêu doanh số và Quản lý bán hàng
để cho phép bạn quản lý mục tiêu doanh số cho nhân viên kinh doanh và đội bán hàng trong ứng dụng Quản lý bán hàng

Nó cũng giúp bạn hiểu rõ hơn về hiệu suất bán hàng so với các mục tiêu với một số chỉ số hiệu suất chính.

1. Mục tiêu doanh số cho nhân viên kinh doanh trong ứng dụng Quản lý bán hàng
    * Nhân viên kinh doanh gửi mục tiêu của họ
    * Đội trưởng bán hàng phê duyệt/điều chỉnh/từ chối mục tiêu
2. Mục tiêu doanh số cho các đội bán hàng trong ứng dụng Quản lý bán hàng
    * Đội trưởng đăng ký mục tiêu doanh số của họ
    * Quản lý bán hàng khu vực có thể phê duyệt/điều chỉnh/từ chối mục tiêu
3. Đo lường mục tiêu bán hàng tự động
    * Dành cho cá nhân/nhân viên kinh doanh
        * Tổng doanh số được xác nhận trong thời gian của mục tiêu
        * Đạt mục tiêu doanh số (tính theo phần trăm (%), dựa trên doanh số được xác nhận)
        * Tổng doanh số đã được lập hóa đơn trong thời gian của mục tiêu
        * Đạt mục tiêu hóa đơn (tính theo phần trăm (%), Dựa trên doanh số hóa đơn được xác nhận)
    * Dành cho đội bán hàng
        * Tổng doanh số được xác nhận trong thời gian của muc tiêu
        * Đạt mục tiêu bán hàng (tính theo phần trăm (%), dựa trên doanh số được xác nhận)
        * Tổng doanh số đã được lập hóa đơn trong thời gian của mục tiêu
        * Đạt mục tiêu hóa đơn (tính theo phần trăm (%), Dựa trên doanh số hóa đơn được xác nhận)
        
Ấn bản hỗ trợ
=============
1. Ấn bản cộng đồng
2. Ấn bản doanh nghiệp

    """,

    'author': "T.V.T Marine Automation (aka TVTMA)",
    'website': 'https://www.tvtmarine.com',
    'live_test_url': 'https://v13demo-int.erponline.vn',
    'support': 'support@ma.tvtmarine.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['sale_crm', 'to_sales_target'],

    # always loaded
    'data': [
        'data/scheduler_data.xml',
        'security/sales_team_security.xml',
        'views/crm_team_views.xml',
        'views/personal_sales_target_views.xml',
        'views/team_sales_target_views.xml',
        'views/assets.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'price': 45.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
