# -*- coding: utf-8 -*-
{
    'name': "HIT Hybrid Customization",

    'summary': """
        Hybrid Customization""",

    'description': """
        Enhancement All Module.
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
    'depends': ['account', 'purchase_request', 'account_asset', 'purchase'],

    # always loaded
    # make sure the menu view is on the last
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_request_views.xml',
        'views/maintenance_request_views.xml',
        'views/account_payment_views.xml',
        # 'views/purchase_order_views.xml',
    ],
}
