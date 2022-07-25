{
    'name': "Sales Teams Advanced",
    'name_vi_VN': "Nhóm bán hàng nâng cao",
    'summary': """
Adding more sales access groups""",
    'summary_vi_VN': """
Thêm nhiều nhóm truy cập bán hàng""",
    'description': """
Larger business organizations usually have multiple sales teams with multiple sales user levels. This module reorganizes the sales groups as below:

* **Sales / User: Own Documents Only**: this is a default group in Odoo.
* **Sales / Sales Team Leader**: new access group that inherits "Sales / User: Own Documents Only"
* **Sales / Regional Manager**: a new access group that inherits the group "Sales / Sales Team Leader"
* **Sales / User: All Documents**: this is a default group in Odoo. It now inherits "Sales / Regional Manager" instead of "Sales / User: Own Documents Only"
* **Sales / Manager**: Full access rights to Sales Management application

Security Policies
-----------------

* **Sales / User: Own Documents Only**: view team of which she or he is a member
* **Sales / Sales Team Leader**: view/edit team of which she or he is either a member or the team leader
* **Sales / Regional Manager**: view/edit/create/delete team of which she or he is either a member or the team leader or the regional manager
* **Sales / User: All Documents**: full access rights for all teams but sales configurations
* **Sales / Manager**: Full access rights to Sales Management application, including doing configuration

NOTES
=====

This module does not create access policies to records in Sales Management application and CRM application yet.
Separated modules will be required, depending on your situation where CRM and/or Sales Management are installed in your Odoo instance. I.e.

* When you have CRM installed, you will need the module "CRM - Sales Teams Advanced": https://apps.odoo.com/apps/modules/13.0/to_sales_team_advanced_crm/
* When you have Sales Management installed, you will need the module "Sales - Sales Teams Advanced": https://apps.odoo.com/apps/modules/13.0/to_sales_team_advanced_sale/

Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,
    'description_vi_VN': """
Module này làm gì
=================

Các tổ chức kinh doanh lớn thường có nhiều nhóm bán hàng với nhiều cấp độ người dùng bán hàng. Module này sắp xếp lại nhóm bán hàng như sau:

* **Bán hàng / Người dùng: Chỉ có tài liệu riêng**: đây là nhóm mặc định trong odoo.
* **Bán hàng / Trưởng nhóm bán hàng**: nhóm truy cập mới kế thừa "Bán hàng / Người dùng: Chỉ có tài liệu riêng"
* **Bán hàng / Người quản lý khu vực**: nhóm truy cập mới kế thừa "Bán hàng / Trưởng nhóm bán hàng"
* **Bán hàng / Người dùng: Tất cả tài liệu**: đây là nhóm mặc định trong odoo.Bây giờ nó kế thừa "Bán hàng / Người quản lý khu vực" thay vì "Bán hàng / Người dùng: Chỉ có tài liệu riêng".
* **Bán hàng / Quản lý**: đầy đủ quyền truy cập vào ứng dụng quản lý bán hàng.

Chính sách bảo mật
------------------

* **Bán hàng / Người dùng: Chỉ có tài liệu riêng**: xem nhóm mà cô ấy hoặc anh ấy là thành viên.
* **Bán hàng / Trưởng nhóm bán hàng**: Xem/chỉnh sửa nhóm mà cô ấy hoặc anh ấy là thành viên hoặc nhóm trưởng.
* **Bán hàng / Người quản lý khu vực**: Xem/chỉnh sửa/xóa/tạo nhóm mà anh ấy hoặc cô ấy là thành viên hoặc nhóm trưởng hoặc người quản lý khu vực.
* **Bán hàng / Người dùng: Tất cả tài liệu**: đầy đủ quyền truy cập cho tất cả các nhóm trừ cấu hình bán hàng.
* **Bán hàng / Quản lý**: đầy đủ quyền truy cập vào ứng dụng quản lý bán hàng, bao gồm cả cấu hình.

Ghi chú
=======

Module này chưa tạo chính sách truy cập vào hồ sơ ứng dụng Quản lý bán hàng và ứng dụng CRM.
Các module riêng biệt sẽ được yêu cầu, tùy thuộc vào tình huống của bạn nơi CRM và/hoặc Quản lý bán hàng được cài đặt trong odoo của bạn.

* Khi bạn đã cài đặt CRM, bạn sẽ cần cài module "CRM - Nhóm bán hàng nâng cao"
* Khi bạn đã cài đặt Quản lý bán hàng, bạn sẽ cần cài module "Bán hàng - Nhóm bán hàng nâng cao"

Ấn bản hỗ trợ
=============
1. Ấn bản cộng đồng
2. Ấn bản doanh nghiệp

    """,
    'images':['images/main_screenshot.png'],
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
    'depends': ['sales_team'],

    # always loaded
    'data': [
        'security/sales_team_security.xml',
        'security/ir.model.access.csv',
        'views/crm_team_region_views.xml',
        'views/crm_team_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 45.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}