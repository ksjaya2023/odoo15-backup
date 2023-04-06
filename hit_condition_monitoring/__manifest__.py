# -*- coding: utf-8 -*-
{
    'name': "HIT Condition Monitoring",

    'summary': """
        For Maintenance Purpose""",

    'description': """
        Condition Monitoring.
    """,

    'author': "twitter.com/thepythoncode",
    'website': "http://www.hitconsulting.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Maintenance',
    'version': '0.1',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'depends': ['maintenance', 'stock'],

    # always loaded
    # make sure the menu view is on the last
    'data': [
        'security/ir.model.access.csv',
    ],
}
