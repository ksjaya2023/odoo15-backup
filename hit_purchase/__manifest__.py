# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

{
    'name': 'hit_purchase',
    'author': 'HIT Digital Indonesia',
    'website': 'http://www.hitconsulting.id',
    'version': '0.1',
    'summary': '''Purchase Customization
    ''',
    'description': '''
        Enhancement Purchase Module.
    ''',
    'category': 'Purchase',
    'license': 'LGPL-3',
    'installable': True,
    'depends': ['maintenance', 'account_accountant', 'purchase', 'stock', 'analytic'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'demo': [],
}
