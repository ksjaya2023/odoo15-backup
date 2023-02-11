# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

{
    "name": "HIT Purchase Request Extended",
    "author": "HIT",
    "version": "0.1",
    "summary": """Entended version of Purchase Request module 
        created by ForgeFlow, Odoo Community Association (OCA)
    """,
    "category": "Purchase Management",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "purchase",
        "product",
        "purchase_stock",
        "purchase_request",
        "analytic",
        # "hit_tpe_migration",
    ],
    "data": [
        # "views/purchase_order_view.xml",
        # "views/purchase_request_view.xml",
        # 'views/purchase_order_view_2.xml',
    ],
    "demo": [],
}
