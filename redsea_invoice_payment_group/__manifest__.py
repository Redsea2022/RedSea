# -*- coding: utf-8 -*-
{
    'name': "redsea_invoice_payment_group",
    'author': "Centione",
    'website': "http://www.centione.com",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/views.xml',
    ]
}
