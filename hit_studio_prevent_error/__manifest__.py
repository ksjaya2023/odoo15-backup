# -*- coding: utf-8 -*-
{
    'name': "HIT Studio Prevent Error",

    'summary': """
        HIT Studio Prevent Error""",

    'description': """
        HIT Studio Prevent Error.
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
    'depends': ['stock'],

    # always loaded
    'data': [],
    # only loaded in demonstration mode
    'demo': [],
}
