# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Product',
    # 'version': '14.0',
    'author': "Santosh",
    'category': 'custom',
    # 'sequence': 51,
    # 'summary': 'Product ',
    'description': """Product, Import Products    """,
    'website': 'https://www.healthgenie.com',
    'depends': ['sale', 'product'],
    'data': [
        'views/product_category_view.xml',
        'views/product_package_view.xml',
        'views/brand_name_view.xml',
        'views/product_template_views.xml',
        'views/sku_mapping_view.xml',
        'wizard/import_products_view.xml',
		'wizard/export_products_view.xml',
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
