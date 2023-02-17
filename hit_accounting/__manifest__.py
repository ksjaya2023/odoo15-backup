# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

{
    'name': 'HIT Accounting',
    'author': 'HIT Digital Indonesia',
    'website': 'http://www.hitconsulting.id',
    'version': '0.1',
    'summary': '''Accounting Customization
    ''',
    'description': '''
        Enhancement Accounting Module.
    ''',
    'category': 'Accounting',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'depends': ['account_accountant',
                'account',
                'contacts',
                'account_asset'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_views.xml',
        'views/account_asset_views.xml',
        'views/account_payment_views.xml',
        'views/process_views.xml',
        'views/activity_views.xml',
        'views/location_views.xml',
        'views/department_views.xml',
        'views/process_activity_views.xml',
        # 'views/res_partner_bank_views.xml',
        'views/hit_accounting_menus.xml',
    ],
    'demo': [],
}
