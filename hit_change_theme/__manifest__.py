# -*- coding: utf-8 -*-
{
    'name': "HIT Change Theme",

    'summary': """
        Change theme""",

    'description': """
        Change theme basic.
    """,

    'author': "HIT Digital Indonesia",
    'website': "http://www.hitconsulting.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customization',
    'version': '0.1',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'depends': ['web'],

    # always loaded
    # make sure the menu view is on the last
    'data': [
        'security/ir.model.access.csv',
        'views/change_theme-views.xml',
        # 'views/maintenance_request_views.xml',
        # 'views/account_payment_views.xml',
        # # 'views/purchase_order_views.xml',
    ],
    'website': "https://www.odoo.com/forum/help-1/odoo-online-homepage-change-background-color-which-i-can-do-using-studio-and-now-i-want-to-change-the-menu-color-170955?forum=forum.forum%281%2C%29&question=forum.post%28170955%2C%29",
}
