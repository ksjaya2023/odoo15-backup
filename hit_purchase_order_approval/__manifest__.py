# -*- coding: utf-8 -*-
{
    'name': "hit_purchase_order_approval",

    'summary': """
        Adding approval to purchase order""",

    'description': """
    """,

    'author': "HIT",
    'website': "http://www.hasnurgroup.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase', 'web_studio', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/assets.xml', NOT WORKING LMAO
        'views/purchase_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
