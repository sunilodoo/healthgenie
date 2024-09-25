# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
# from odoo.tools import amount_to_text_en, float_round
# from datetime import datetime, timedelta
# from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class ProductBrand(models.Model):
	_name = "product.brand"
	_description="Brand of product name"
	name = fields.Char(string="Brand")

class ProductCategory1(models.Model):
	_name = "product.category1"
	_description="Product Category1"
	name = fields.Char(string="Product Category1")
class ProductCategory2(models.Model):
	_name = "product.category2"
	_description="Product Category2"
	name = fields.Char(string="Product Category2")
class ProductCategory3(models.Model):
	_name = "product.category3"
	_description="Product Category3"
	name = fields.Char(string="Product Category3")

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	model_no = fields.Char('Model No.')
	model_name = fields.Char('Model Name.')
	product_specification = fields.Char('Product Specification')
	product_material = fields.Char('Product Material')
	supplier_name = fields.Char('Supplier Name')
	product_box_dimension_l = fields.Float('Product Box dim L')
	product_box_dimension_b = fields.Float('Product Box dim B')
	product_box_dimension_h = fields.Float('Product Box dim H')
	prod_box_grs_wt_kgs = fields.Float('Product Box grs wt kgs')
	prod_box_net_wt_kgs = fields.Float('Producr Box net wt kgs')
	carton = fields.Char('Pcs/M Carton')
	mc_dimm_l_cms = fields.Float('MC dimm L cms')
	mc_dimm_b_cms = fields.Float('MC dimm B cms')
	mc_dimm_h_cms  = fields.Float('MC dimm H cms')
	mc_Grs_wt_l_kgs = fields.Float('MC Grs wt L kgs')
	mc_net_wt_kgs = fields.Float('MC net wt kgs')
	mc_vol_cbm = fields.Float('MC  Vol CBM')
	product_type = fields.Selection([
		('raw_material', 'Raw Material'),
		('packing', 'Packing'),
		('finish_goods', 'Finished Goods'),
		('consumable', 'Consumable')
		], string="Product Type", store=True)

	default_code = fields.Char('Product SKU Code', index=True)
	categ1 = fields.Many2one('product.category1', string='Product Category-1', compute='_compute_categ1', inverse='_set_categ1', store=True)
	categ2 = fields.Many2one('product.category2', string='Product Category-2', compute='_compute_categ2', inverse='_set_categ2', store=True)
	categ3 = fields.Many2one('product.category3', string='Product Category-3', compute='_compute_categ3', inverse='_set_categ3', store=True)
	sale_type = fields.Selection([
        ('assemble_packing', 'Assemble-Packing'),
        ('import', 'Import'),
        ('mfg', 'Mfg'),
        ('mfg_packing', 'Mfg-Packing'),
        ('trading', 'Trading'),
        ('trading_packing', 'Trading-Packing')
        ], string="Sale Type", compute='_compute_sale_type', inverse='_set_sale_type', store=True)
	brand_id = fields.Many2one('product.brand', string="Brand", compute='_compute_brand_id', inverse='_set_brand_id', store=True)
	p_prepartion_id = fields.Selection([
        ('assemble_packing', 'Assemble-Packing'),
        ('import', 'Import'),
        ('mfg', 'Mfg'),
        ('mfg_packing', 'Mfg-Packing'),
        ('trading', 'Trading'),
        ('trading_packing', 'Trading-Packing')
        ], string="Product Preparation Type", compute='_compute_p_prepartion_id', inverse='_set_p_prepartion_id', store=True)
	_sql_constraints = [
	('default_code_unique', 'unique(default_code)', "A Internal Reference can only be assigned to one product !")
	]
	@api.depends('product_variant_ids', 'product_variant_ids.categ1')
	def _compute_categ1(self):
		unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
		for template in unique_variants:
			template.categ1 = template.product_variant_ids.categ1
		for template in (self - unique_variants):
			template.categ1 = False
	def _set_categ1(self):
		for template in self:
			if len(template.product_variant_ids) == 1:
				template.product_variant_ids.categ1 = template.categ1

	@api.depends('product_variant_ids', 'product_variant_ids.categ2')
	def _compute_categ2(self):
		unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
		for template in unique_variants:
			template.categ2 = template.product_variant_ids.categ2
		for template in (self - unique_variants):
			template.categ2 = False
	def _set_categ2(self):
		for template in self:
			if len(template.product_variant_ids) == 1:
				template.product_variant_ids.categ2 = template.categ2

	@api.depends('product_variant_ids', 'product_variant_ids.categ3')
	def _compute_categ3(self):
		unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
		for template in unique_variants:
			template.categ3 = template.product_variant_ids.categ3
		for template in (self - unique_variants):
			template.categ3 = False
	def _set_categ3(self):
		for template in self:
			if len(template.product_variant_ids) == 1:
				template.product_variant_ids.categ3 = template.categ3

	@api.depends('product_variant_ids', 'product_variant_ids.sale_type')
	def _compute_sale_type(self):
		unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
		for template in unique_variants:
			template.sale_type = template.product_variant_ids.sale_type
		for template in (self - unique_variants):
			template.sale_type = False
	def _set_sale_type(self):
		for template in self:
			if len(template.product_variant_ids) == 1:
				template.product_variant_ids.sale_type = template.sale_type

	@api.depends('product_variant_ids', 'product_variant_ids.brand_id')
	def _compute_brand_id(self):
		unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
		for template in unique_variants:
			template.brand_id = template.product_variant_ids.brand_id
		for template in (self - unique_variants):
			template.brand_id = False
	def _set_brand_id(self):
		for template in self:
			if len(template.product_variant_ids) == 1:
				template.product_variant_ids.brand_id = template.brand_id

	@api.depends('product_variant_ids', 'product_variant_ids.p_prepartion_id')
	def _compute_p_prepartion_id(self):
		unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
		for template in unique_variants:
			template.p_prepartion_id = template.product_variant_ids.p_prepartion_id
		for template in (self - unique_variants):
			template.p_prepartion_id = False
	def _set_p_prepartion_id(self):
		for template in self:
			if len(template.product_variant_ids) == 1:
				template.product_variant_ids.p_prepartion_id = template.p_prepartion_id

	@api.model_create_multi
	def create(self, vals_list):
		''' Store the initial standard price in order to be able to retrieve the cost of a product template for a given date'''
		templates = super(ProductTemplate, self).create(vals_list)
		if "create_product_product" not in self._context:
			templates._create_variant_ids()
		# This is needed to set given values to first variant after creation
		for template, vals in zip(templates, vals_list):
			related_vals = {}
			if vals.get('barcode'):
				related_vals['barcode'] = vals['barcode']
			if vals.get('default_code'):
				related_vals['default_code'] = vals['default_code']
			# if vals.get('categ1'):
			# 	related_vals['categ1'] = vals['categ1']
			# if vals.get('categ2'):
			# 	related_vals['categ2'] = vals['categ2']
			# if vals.get('categ3'):
			# 	related_vals['categ3'] = vals['categ3']
			# if vals.get('sale_type'):
			# 	related_vals['sale_type'] = vals['sale_type']
			if vals.get('brand_id'):
				related_vals['brand_id'] = vals['brand_id']
			if vals.get('p_prepartion_id'):
				related_vals['p_prepartion_id'] = vals['p_prepartion_id']
			if vals.get('standard_price'):
				related_vals['standard_price'] = vals['standard_price']
			if vals.get('volume'):
				related_vals['volume'] = vals['volume']
			if vals.get('weight'):
				related_vals['weight'] = vals['weight']
				# Please do forward port
			if vals.get('packaging_ids'):
				related_vals['packaging_ids'] = vals['packaging_ids']
			if related_vals:
				template.write(related_vals)
		return templates


class ProductProduct(models.Model):
	_inherit = 'product.product'

	model_no = fields.Char('Model No.')
	model_name = fields.Char('Model Name.')
	product_specification = fields.Text('Product Specification')
	product_material = fields.Char('Product Material')
	supplier_name = fields.Char('Supplier Name')
	product_box_dimension_l = fields.Float('Product Box dim L')
	product_box_dimension_b = fields.Float('Product Box dim B')
	product_box_dimension_h = fields.Float('Product Box dim H')
	prod_box_grs_wt_kgs = fields.Float('Product Box grs wt kgs')
	prod_box_net_wt_kgs = fields.Float('Producr Box net wt kgs')
	carton = fields.Char('Pcs/M Carton')
	mc_dimm_l_cms = fields.Float('MC dimm L cms')
	mc_dimm_b_cms = fields.Float('MC dimm B cms')
	mc_dimm_h_cms = fields.Float('MC dimm H cms')
	mc_Grs_wt_l_kgs = fields.Float('MC Grs wt L kgs')
	mc_net_wt_kgs = fields.Float('MC net wt kgs')
	mc_vol_cbm = fields.Float('MC  Vol CBM')

	sku_id = fields.Char(string="SKU ID")
	categ1 = fields.Many2one('product.category1', string='Product Sub Category')
	categ2 = fields.Many2one('product.category2', string='Product Category')
	categ3 = fields.Many2one('product.category3', string='Product Sub Category')
	type_of_product = fields.Many2one('product.type', string="Product Type")
	sale_type = fields.Selection([
		('assemble_packing', 'Assemble-Packing'),
		('import', 'Import'),
		('mfg', 'Mfg'),
		('mfg_packing', 'Mfg-Packing'),
		('trading', 'Trading'),
		('trading_packing', 'Trading-Packing')
	], string="Sale Type")
	product_package_line_id = fields.One2many('product.package', 'name', string="Product Pack")
	brand_id = fields.Many2one('product.brand', string="Brand")
	p_prepartion_id = fields.Selection([
		('assemble_packing', 'Assemble-Packing'),
		('import', 'Import'),
		('mfg', 'Mfg'),
		('mfg_packing', 'Mfg-Packing'),
		('trading', 'Trading'),
		('trading_packing', 'Trading-Packing')
	], string="Product Preparation Type")
	# taxes_id = fields.Many2many(related="product_tmpl_id.taxes_id", string="Taxes Id")
	# _sql_constraints = [
	# ('default_code_uniq', 'unique(default_code)', "A Internal Reference can only be assigned to one product !")
