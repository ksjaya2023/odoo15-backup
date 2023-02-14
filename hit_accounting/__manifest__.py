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
                'account'],
    'data': [
        'security/ir.model.access.csv',
        # 'views/views.xml',
    ],
    'demo': [],
}
