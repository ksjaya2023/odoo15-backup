# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

{
    'name': 'HIT Menu Access Right',
    'author': 'HIT Digital Indonesia',
    'website': 'http://www.hitconsulting.id',
    'version': '0.1',
    'summary': '''
        Menu Access Right
    ''',
    'description': '''
        Enhancement Accounting Module.
    ''',
    'category': 'Access Right',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'depends': ['purchase_request'],
    'data': [
        'security/hit_account_security.xml',
        'security/ir.model.access-hit-purchasing.csv',
        'views/hit_account_menu_view.xml',
    ],
    'demo': [],
}
