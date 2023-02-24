# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

{
    'name': 'HIT Purchase',
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
    'application': True,
    'depends': ['purchase',
                'maintenance',
                'account_accountant',
                'stock',
                'analytic',
                'uom',
                'hit_maintenance',
                'purchase_request'],
    'data': [
        'security/ir.model.access.csv',
        'data/po_sequence.xml',
        'data/pr_sequence.xml',
        'data/rfq_sequence.xml',
        'data/stock_code_sequence.xml',
        'views/purchase_order_views.xml',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        'views/res_partner_views.xml',
    ],
    'demo': [],
}
