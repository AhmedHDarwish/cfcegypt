{
    'name': "Sales Target Management",
    'name_vi_VN': "Quản lý mục tiêu doanh số",

    'summary': """
Sales targets for individual sales persons and sales teams.
""",
    'summary_vi_VN': """
Mục tiêu doanh số cho nhân viên kinh doanh và đội bán hàng.
""",
    'description': """
Manage Sales Targets for your sales persons and sales teams; Ready to get extended in other applications

Key Features
============
1. Multiple Sales Groups in well organized manner, thanks to depending on the application `Sales Teams Advanced`
    * Sales / User: Own Documents Only
    * Sales / Sales Team Leader
    * Sales / Regional Manager
    * Sales / User: All Documents
    * Sales / Manager
2. Submit and Approval Process
    * Individual Targets
        * Sales persons register their own target.
        * Sales Team Leader can either approve or refuse and request changes
    * Team Targets
        * Team Leader register their team's sales target
        * Regional Sales Manager can either approve or refuse and request changes
3. Communication on targets to improve productivity thanks to the Odoo's native mail thread
    * Managers leave comments, request changes, etc
    * Submitters explain, ask for recommendation, etc
4. Ready for extending in sales related application:
    * Auto target reach measurement for Sales: https://apps.odoo.com/apps/modules/12.0/to_sales_target_sale
    * Auto target reach measurement for Points of Sales: https://apps.odoo.com/apps/modules/12.0/to_sales_target_pos

Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,
    'description_vi_VN': """
Quản lý mục tiêu doanh số cho nhân viên kinh doanh và đội bán hàng; Sẵn sàng để mở rộng trong ứng dụng khác

Module này làm gì
=================

1. Nhiều nhóm bán hàng được tổ chức tốt nhờ vào ứng dụng "Nhóm bán hàng nâng cao"
    * Bán hàng / Người dùng: Own Documents Only
    * Bán hàng / Trường nhóm bán hàng
    * Bán hàng / Người quản lý khu vực
    * Bán hàng / Người dùng: Tất cả tài liệu
    * Bán hàng / Quản lý

2. Quy trình nộp và phê duyệt
    * Mục tiêu cá nhân
        * Người bán hàng đăng kí mục tiêu riêng của họ
        * Trưởng nhóm bán hàng có thể phê duyệt hoặc từ chối và yêu cầu thay đổi
    * Mục tiêu nhóm
        * Trưởng nhóm đăng ký mục tiêu nhóm của họ
        * Người quản lý khu vực có thể phê duyệt hoặc từ chối và yêu cầu thay đổi

3. Liên lạc các mục tiêu để cải thiện năng suất nhờ vào các chủ đề thư của odoo
    * Người quản ly để lại nhận xét, ý kiến thay đổi, ...
    * Người gủi giải thích, yêu cầu cho đề xuất, ...

4. Sẵn sàng cho việc mở rộng ứng dụng liên quan đến bán hàng:
    * Đo lường mục tiêu tự động cho doanh số
    * Đo lường mục tiêu tự động cho điểm bán hàng

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
    'depends': ['to_sales_team_advanced','account'],

    # always loaded
    'data': [
        'security/sales_team_security.xml',
        'security/ir.model.access.csv',
        'views/root_menu.xml',
        'views/sales_commission_model.xml',
        'views/team_sales_target_views.xml',
        'views/personal_sales_target_views.xml',
        'views/crm_team_views.xml',
    ],
    'installable': True,
    'application': True, # set this True after upgrading for Odoo 13
    'auto_install': False,
    'price': 45.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
