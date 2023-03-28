# -*- coding: utf-8 -*-
{
    'name': "hit_res_partner",

    'summary': """
        Custom module to handle migration res.partner""",

    'description': """
        Custom module to handle migration from res.partner
    """,

    'author': "anggakawa",
    'website': "http://www.hasnurgroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
