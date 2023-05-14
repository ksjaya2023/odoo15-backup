# -*- coding: utf-8 -*-
{
    'name': "HIT Inventrory",

    'summary': """
        hit_inventrory in Products""",

    'description': """
        hit_inventrory Module customization.
    """,

    'author': "HIT Digital Indonesia",
    'website': "http://www.hitconsulting.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory/Inventory',
    'version': '0.1',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['stock',
                'account',
                'hit_maintenance',
                'purchase_request'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/inventory_issued_sequence.xml',
        'data/inventory_receipt_sequence.xml',
        'data/inventory_return_sequence.xml',
        'data/inventory_transfer_rev_sequence.xml',
        'data/inventory_transfer_trf_sequence.xml',
        'data/number_gi_sequence.xml',
        # 'views/views.xml',
        'views/stock_picking_views.xml',
        'views/stock_quant_views.xml',
        'views/stock_move_views.xml',
        'views/product_category_views.xml',
        'views/product_template_views.xml',
        'views/stock_valuation_layer_views.xml',
        'views/bin_location_views.xml',
        'views/product_class_views.xml',
        'views/stock_type_views.xml',
        'views/hit_inventory_menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
