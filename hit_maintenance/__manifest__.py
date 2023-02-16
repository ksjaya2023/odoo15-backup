# -*- coding: utf-8 -*-
{
    'name': "HIT Maintenance",

    'summary': """
        Maintenance Customization""",

    'description': """
        Enhancement Maintenance Module.
    """,

    'author': "HIT Digital Indonesia",
    'website': "http://www.hitconsulting.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Maintenance',
    'version': '0.1',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'depends': ['maintenance',
                'account_accountant',
                'purchase',
                'stock',
                'analytic',
                'account',
                'hit_accounting',
                'product',
                'purchase_stock'],

    # always loaded
    # make sure the menu view is on the last
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_request_views.xml',
        'views/maintenance_equipment_views.xml',
        'views/reservation_views.xml',
        'views/return_request_views.xml',
        'views/measuring_equipment_views.xml',
        'views/eqp_class_views.xml',
        'views/brand_views.xml',
        'views/unit_model_views.xml',
        'views/engine_model_views.xml',
        'views/eqp_attachment_views.xml',
        'views/eqp_attachment_product.xml',
        'views/eqp_status_views.xml',
        'views/hit_maintenance_menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
