# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.exceptions import Warning, UserError

class SkuMapping(models.Model):
	_name = 'sku.mapping'
	_description = 'SKU Mapping'
	# _order = 'sequence'
	# _order = "name desc"
	_sql_constraints = [
	('unique_name', 'unique(name)', "A SKU can only be assigned to one product !")
	]
	pro_pro_id = fields.Many2one('product.product', string='SKU Reference')
	name = fields.Char(string="SKU ID", required=True)
	product_id = fields.Many2one(related='pro_pro_id', string="Product Name.")
	default_code = fields.Char(related="pro_pro_id.default_code", string="Product Id")
	product_tmpl_id = fields.Many2one(related="pro_pro_id.product_tmpl_id", string="Product Temp Id")
	portal_id_type = fields.Selection([('asin', 'ASIN'), ('fsn', 'FSN')], string="Portal ID Type")
	id_number = fields.Char(string="ID Number")