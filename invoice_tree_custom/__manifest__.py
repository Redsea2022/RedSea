# -*- coding: utf-8 -*-
{
    'name': "invoice_tree_custom",
    'author': "Centione",
    'website': "http://www.centione.com",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ]
}
