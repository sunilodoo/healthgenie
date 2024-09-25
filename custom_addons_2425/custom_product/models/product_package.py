# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.exceptions import Warning, UserError

class ProductPackage(models.Model):
	_name = 'product.package'
	_description = 'Product Package'
	# pro_pro_id = fields.Many2one('product.product', string='Product Package')
	name = fields.Many2one('product.product', string='Product Name')
	default_code = fields.Char(related="name.default_code", string="Product Id")
	quantity = fields.Float(string="Quantity", required=True)
	# product_id = fields.Many2one(related='pro_temp_id', string="Product ID")
	# product_tmpl_id = fields.Many2one(related="pro_pro_id.product_tmpl_id", string="Product Temp Id")
	# portal_id_type = fields.Selection([('asin', 'ASIN'), ('fsn', 'FSN')], string="Portal ID Type")
	# id_number = fields.Char(string="ID Number")