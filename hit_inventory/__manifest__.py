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
        # 'views/views.xml',
        'views/stock_picking_views.xml',
        'views/stock_quant_views.xml',
        'views/stock_move_views.xml',
        'views/product_category.xml',
        'views/product_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
