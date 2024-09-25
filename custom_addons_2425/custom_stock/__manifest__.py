# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Stock',
    # 'version': '14.0',
    'author': "Santosh Singh",
    'category': 'custom',
    # 'sequence': 51,
    # 'summary': 'Stock',
    'description': """Stock

    """,
    'website': 'https://www.healthgenie.com',
    'depends': ['stock','account','sale'],
    'data': [
        'views/stock_inherit_views.xml',
        'views/stock_transfer_view.xml',
        'views/stock_transfer_sale_view.xml',
        'views/stock_transfer_purchase_view.xml',
        'views/return_order_view.xml',
        'data/ir_sequence_data.xml',
        'wizard/import_return_order_view.xml',
        'wizard/import_warehouse_view.xml',
        'wizard/import_stock_transfer_view.xml',
        'wizard/stock_transfer_excel_report_view.xml',
        'wizard/return_order_excel_report_view.xml',
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
