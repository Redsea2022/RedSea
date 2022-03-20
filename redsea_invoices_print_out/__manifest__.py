# -*- coding: utf-8 -*-
{
    'name': "redsea_invoices_print_out",


    # any module necessary for this one to work correctly
    'depends': ['base','account','web'],

    # always loaded
    'data': [

        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'reports/daily_unloading_returns.xml',
        'reports/freight.xml',
        'reports/outbound_ground_operations.xml',
        'reports/shipping_returns.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
