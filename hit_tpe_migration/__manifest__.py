# -*- coding: utf-8 -*-
{
    'name': "hit_tpe_migration",

    'summary': """
        Kumpulan module untuk migrasi TPE""",

    'description': """
        Kumpulan module untuk migrasi TPE
    """,

    'author': "Angga Kawa",
    'website': "http://www.hasnurgroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customization',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'hit_master_data',
        'hit_inventory_transfer',
        'hit_product_material',
        'hit_purchase_master',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
