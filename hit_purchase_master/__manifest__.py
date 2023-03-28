# -*- coding: utf-8 -*-
{
    "name": "hit_purchase_master",
    "summary": """
        Untuk penambahan menu Master Data di Purchase""",
    "description": """
        Penambahan master data di modul purchase
    """,
    "author": "Angga Kawa",
    "website": "http://www.hasnurgroup.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Customizations",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "purchase", "stock", "hit_master_data"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/purchaser_view.xml",  # purchaser view harus yang paling awal karena menu root ada di sini.
        "views/scope_of_supply_view.xml",
        "views/purchasing_group_view.xml",
        "views/pr_type_view.xml",
        "views/po_type_view.xml",
        "views/order_type_view.xml",
        "views/project_view.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        # "demo/demo.xml",
    ],
}
