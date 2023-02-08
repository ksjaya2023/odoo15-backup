# -*- coding: utf-8 -*-
{
    'name': "Reservation",

    'summary': """
        Reservation in Maintenance""",

    'description': """
        Reservation Module customization.
    """,

    'author': "HIT Digital Indonesia",
    'website': "http://www.hitconsulting.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'HDI',
    'version': '0.1',
    'license': 'LGPL-3',
    'installable': True,

    # any module necessary for this one to work correctly
    'depends': ['maintenance'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
