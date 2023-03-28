# -*- coding: utf-8 -*-
{
    "name": "hit_purchase_enhancement",
    "summary": """
        HIT Purchase Enhancement - Discount and freight cost""",
    "description": """
    """,
    "author": "Angga Kawa",
    "website": "http://www.hasnurgroup.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": [
        "purchase",
        "purchase_stock",
        # "web_studio",
        "stock_account",
        "account",
        "stock",
    ],
    # always loaded
    "data": [
        "report/purchase_reports.xml",
        "views/purchase_order_line.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
}
