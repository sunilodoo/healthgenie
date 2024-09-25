# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Sales',
    # 'version': '12.0',
    'author': "Santosh",
    'category': 'custom',
    # 'sequence': 51,
    # 'summary': 'Sales',
    'description': """Sales

    """,
    'website': 'https://www.healthgenie.com',
    'depends': ['sale', 'sale_stock'],
    'data': [
        'views/sale_order_views.xml',
        'views/sale_order_missing_views.xml',
		'wizard/sale_order_import_view.xml',
		'wizard/sale_order_report_view.xml',
        'wizard/sale_order_create_invoices_view.xml',
        'security/ir.model.access.csv',
    ],
    'test': [
        
    ],
    'demo': [
       
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
