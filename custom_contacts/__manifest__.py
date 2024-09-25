# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Contacts',
    # 'version': '14.0',
    'author': "Santosh Singh",
    'category': 'custom',
    # 'sequence': 51,
    # 'summary': 'Stock',
    'description': """ All State with pincode. 

    """,
    'website': 'https://www.healthgenie.com',
    'depends': ['contacts','sale'],
    'data': [
        'views/contacts_inherit_views.xml',
        'views/res_portal_views.xml',
        'wizard/import_pincode_view.xml',
        'wizard/sales_payment_view.xml',
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
