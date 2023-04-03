# -*- coding: utf-8 -*-
{
    'name': "hit_master_data",

    'summary': """
        Custom module to handle migration from Odoo Studio""",

    'description': """
        Custom module to handle migration from x_project_master_data,
        wbs etc
    """,

    'author': "anggakawa",
    'website': "http://www.hasnurgroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'hit_res_partner', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/project_view.xml',
        'views/wbs_view.xml',
        'views/contract_management_view.xml',
        'views/account_move_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
