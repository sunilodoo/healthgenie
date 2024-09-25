# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
# from openerp.tools.translate import _
# from openerp import tools, api
# from openerp import SUPERUSER_ID
# from datetime import datetime, timedelta
import csv
# import tempfile
# import StringIO
import io
import base64
import datetime as dt
from odoo.exceptions import Warning, UserError
import logging

_logger = logging.getLogger(__name__)


class ImportProducts(models.TransientModel):
	_name = 'import.products'
	_description = 'Import products'

	product_file = fields.Binary(string='CSV File', help='File should be separated by comma (,) and quoted using Quote character (") ')

	# def sku_update(self):
	# 	prod_pool = self.env['product.template']
	# 	# u_o_m_pool = self.env['uom.uom']
	# 	f = base64.b64decode(self.product_file)
	# 	data_file = io.StringIO(f.decode("utf-8"))
	# 	reader = csv.reader(data_file, delimiter=',')
	# 	headers = {}
	# 	for row in reader:
	# 		col_count = 0
	# 		for col in row:
	# 			headers[col] = col_count
	# 			col_count = col_count + 1
	# 		break;
	# 	current_pro_pro_id = ''
	# 	current_magento_id = ''
	# 	count =1
	# 	for row in reader:
	# 		magento_exist = False
	# 		magento_id = row[headers['Magento_ID']].strip() if row[headers['Magento_ID']] else ''
	# 		if magento_id:
	# 			pro_pro_id = self.env['product.product'].search([('default_code', '=', magento_id)])
	# 			if pro_pro_id:
	# 				current_pro_pro_id = pro_pro_id[0]
	# 				current_magento_id = magento_id
	# 				magento_exist = True
	# 			else:
	# 				magento_exist = False
	# 		if not (current_magento_id or magento_id):
	# 			magento_exist = False
	# 		if magento_exist:
	# 		# if current_magento_id or magento_id:
	# 			vals = {}
	# 			sk = row[headers['SKU ID']].strip() if row[headers['SKU ID']] else ''
	# 			sku_id = self.env['sku.mapping'].search([('name', '=', sk)])
	# 			if sku_id:
	# 			else:
	# 				if sk:
	# 					vals['sku_line_id'] = [(0,0,{'name': sk})]
	# 				# sku_name = row[headers['SKU ID']].strip()
	# 				# rec.update({'sku_line_id':[(0,0,{'name': sku_name})]})
	# 				# count = count+1
	# 			vals['asin'] = row[headers['ASIN']].strip() if row[headers['ASIN']] else ''
	# 			# vals['fsn'] = row[headers['FSN']].strip() if row[headers['FSN']] else ''
	# 			pro_update = current_pro_pro_id.update(vals)
	# 			count = count+1
	# 		else:
	# 			count+=1
	# 			raise Warning(_("The Magento_ID -----"+row[headers['Magento_ID']].strip()+"-----is not found---------"))

	def update(self):
		print("-------------------123--------update--------------------------")
		f = base64.b64decode(self.product_file)
		data_file = io.StringIO(f.decode("utf-8"))
		reader = csv.reader(data_file, delimiter=',')
		headers = {}
		for row in reader:
			col_count = 0
			for col in row:
				headers[col] = col_count
				col_count = col_count + 1
			break;
		#----------------------------------------------------one-time-check----------------------------------------------------
		inv_line_ids = self.env['account.move.line'].search([])
		for rec in inv_line_ids:
			rec.update({'sku_name': rec.product_id.default_code})
		print("---------------------inv-----------comp--------------")
		inv_line_ids = self.env['sale.order.line'].search([])
		for rec in inv_line_ids:
			rec.update({'sku_name': rec.product_id.default_code})
		print("---------------------so-----------comp--------------")
		#----------------------------------------------------one-time-check----------------------------------------------------
		# count=2
		# for row in reader:
		# 	count+=1
		# 	amz_order_id = row[headers['amazon-order-id']].strip()
		# 	print("---------------amz_order_id--")
		# 	sale_order_id = self.env['account.move'].search([('order_id', '=', amz_order_id)])
		# 	# print("--------------sale_order_id--", sale_order_id)
		# 	if sale_order_id:
		# 		sale_order_id.update({'month_of_sale': 'jul'})
		# 		sale_order_id.so_id.update({'month_of_sale': 'jul'})
		#----------------------------------------------------one-time-check----------------------------------------------------
		# count =1
		# for row in reader:
		# 	count+=1
		# 	amz_order_id = row[headers['amazon-order-id']].strip()
		# 	sale_order_id = self.env['sale.order'].search([('order_id', '=', amz_order_id)])
		# 	# print("--------------sale_order_id--", sale_order_id)
		# 	if sale_order_id:
		# 		if not sale_order_id.partner_id.state_id:
		# 			print("-------------row[headers['ship-postal-code']].strip()----", row[headers['ship-postal-code']].strip())
		# 			p_c = self.env['pincode.state'].search([('name', '=', row[headers['ship-postal-code']].strip())])
		# 			update = sale_order_id.partner_id.update({'state_id': p_c.state_id.id})
		# 			print("-------------update----", update)
		# 			print("-------------p_c----", p_c)
		#---------------------------------------------------------------------------------------------------------------------------
	# def do_import(self):
	# 	# print("-----------------------------------------------------------------------------------------------------------------------------")
	# 	prod_pool = self.env['product.template']
	# 	# u_o_m_pool = self.env['uom.uom']
	# 	f = base64.b64decode(self.product_file)
	# 	data_file = io.StringIO(f.decode("utf-8"))
	# 	reader = csv.reader(data_file, delimiter=',')
	# 	headers = {}
	# 	for row in reader:
	# 		col_count = 0
	# 		for col in row:
	# 			headers[col] = col_count
	# 			col_count = col_count + 1
	# 		break;
	# 	count = 1
	# 	product = ''
	# 	attri_name = ''
	# 	p_t_line_id = ''
	# 	count =1
	# 	for row in reader:
	# 		# product = self.env['product.template'].search([('name', '=', 
	# 		if_product = row[headers['Magento ID']].strip() if row[headers['Magento ID']] else ''
	# 		if if_product:
	# 			prod_vals = {
	# 				'name': row[headers['Name']].strip(),
	# 				'sale_ok': True,
	# 				'purchase_ok': True,
	# 				'type': 'consu',
	# 				'categ_id': self.env['product.category'].search([('name', '=', 'All')]).id,
	# 				'default_code': row[headers['Magento ID']].strip() if row[headers['Magento ID']] else '',
	# 				'l10n_in_hsn_code': row[headers['HSN']].strip() if row[headers['HSN']] else '',
	# 				'taxes_id': [(4, self.env['account.tax'].search([('name', '=', row[headers['Tax']]), ('type_tax_use', '=', 'sale')])[0].id)],
	# 				'p_prepartion_id': row[headers['Sale Type']].strip() if row[headers['Sale Type']] else '',
	# 				'invoice_policy': 'order'
	# 			}
	# 			pro_brand_id = self.env['product.brand'].search([('name', '=', row[headers['Brand']])])
	# 			if not pro_brand_id:
	# 				p_b_i = self.env['product.brand'].create({'name' : row[headers['Brand']]})
	# 				prod_vals['brand_id'] = p_b_i.id
	# 			else:
	# 				prod_vals['brand_id'] = pro_brand_id[0].id
	# 			# print("------------------prod_vals-----------------------------", prod_vals)
	# 			is_product = self.env['product.template'].search([('default_code', '=', if_product)])
	# 			if not is_product:
	# 				product_create = self.env['product.template'].create(prod_vals)
	# 				# y_w = product_create.write({'asin' : row[headers['ASIN']].strip()})
	# 				# print("------------------product_create-------------", product_create)
	# 				# print("------------------y_w-------------", y_w)
	# 				# print("------------------count-------------", count)
	# 			else:
	# 				# is_product.write(prod_vals)
	# 				raise Warning(_("The Product------------ "+row[headers['default_code']]+' is already created. Please update it in line.'+" "+str(count)))
	# 			count = count+1
	# 		else:
	# 			raise Warning(_("----------The Product must have a megento ID------------ "))

	def import_product(self):
		prod_pool = self.env['product.template']
		f = base64.b64decode(self.product_file)
		data_file = io.StringIO(f.decode("utf-8"))
		reader = csv.reader(data_file, delimiter=',')
		headers = {}
		for row in reader:
			col_count = 0
			for col in row:
				headers[col] = col_count
				col_count = col_count + 1
			break;
		count = 1
		product = ''
		attri_name = ''
		p_t_line_id = ''
		count =1
		for row in reader:
			print("------------------------------p1--------------------------", row[headers['Name']])
			print("------------------------------TAX-------------------------", row[headers['Tax']])
			prod_vals = {
					'name': row[headers['Name']].strip(),
					'sale_ok': True,
					'purchase_ok': True,
					'type': 'consu',
					'list_price': 0.0,
					'standard_price': 0.0,
					'categ_id': self.env['product.category'].search([('name', '=', 'All')]).id,
					'default_code': row[headers['Internal Reference']].strip(),
					'l10n_in_hsn_code': row[headers['HSN']].strip(),
					'taxes_id': [(4, self.env['account.tax'].search([('name', '=', row[headers['Tax']]), ('type_tax_use', '=', 'sale')])[0].id)],
					'invoice_policy': 'order'
			}
			# print('----dictionary----', prod_vals)
			brand = row[headers['Brand']].strip()
			pro_brand_id = self.env['product.brand'].search([('name', '=', brand)])
			if not pro_brand_id:
				p_b_i = self.env['product.brand'].create({'name' : brand})
				prod_vals['brand_id'] = p_b_i.id
			else:
				prod_vals['brand_id'] = pro_brand_id[0].id
			ppi = row[headers['PPT']].strip()
			if ppi == 'Assemble-Packing':
				prod_vals['p_prepartion_id'] = 'assemble_packing'
			elif ppi == 'Import':
				prod_vals['p_prepartion_id'] = 'import'
			elif ppi == 'Mfg':
				prod_vals['p_prepartion_id'] = 'mfg'
			elif ppi == 'Mfg-Packing':
				prod_vals['p_prepartion_id'] = 'mfg_packing'
			elif ppi == 'Trading':
				prod_vals['p_prepartion_id'] = 'trading'
			elif ppi == 'Trading-Packing':
				prod_vals['p_prepartion_id'] = 'trading_packing'
			# print("----------prod_vals-------", prod_vals)
			p_c = prod_pool.create(prod_vals)
			# print("--------p_c--------------", p_c)
			count = count+1
			print("------------------------count---------------", count)

	def sku_update2(self):
		prod_pool = self.env['product.product']
		f = base64.b64decode(self.product_file)
		data_file = io.StringIO(f.decode("utf-8"))
		reader = csv.reader(data_file, delimiter=',')
		headers = {}
		for row in reader:
			col_count = 0
			for col in row:
				headers[col] = col_count
				col_count = col_count + 1
			break;
		current_pro_pro_id = ''
		current_magento_id = ''
		count =1
		for row in reader:
			pro_pro_id = self.env['product.product'].search([('default_code', '=', row[headers['Product Id']].strip())])
			sku_vals = {
				'name': row[headers['SKU ID']].strip(),
				# 'id_number': row[headers['ID Number']].strip()
			}
			# p_i_t = row[headers['Portal ID Type']].strip()
			# if p_i_t:
			# 	if p_i_t == 'ASIN':
			# 		sku_vals['portal_id_type'] = 'asin'
			# 		sku_vals['id_number'] = row[headers['ID Number']].strip() if row[headers['ID Number']] else ''
			# 	if p_i_t == 'FNS':
			# 		sku_vals['portal_id_type'] = 'fsn'
			# 		sku_vals['id_number'] = row[headers['ID Number']].strip() if row[headers['ID Number']] else ''
			# print("----------sku_vals-------", sku_vals)
			pro_pro_id.update({'sku_line_id': [(0,0, sku_vals)]})
			# print("----------pro_pro_id-------", pro_pro_id)
			count = count+1
			print("------------------------count---------------", count)

	def fsn_update(self):
		prod_pool = self.env['product.product']
		f = base64.b64decode(self.product_file)
		data_file = io.StringIO(f.decode("utf-8"))
		reader = csv.reader(data_file, delimiter=',')
		headers = {}
		for row in reader:
			col_count = 0
			for col in row:
				headers[col] = col_count
				col_count = col_count + 1
			break;
		current_pro_pro_id = ''
		current_magento_id = ''
		count =1
		for row in reader:
			asin = row[headers['ASIN']].strip()
			if not asin:
				raise Warning(_("ASIN "+' is not '+' in line '+str(count)+' is not found. '))
			sku_id = row[headers['SKU']].strip()
			if not sku_id:
				raise Warning(_("SKU"+' is not '+' in line '+str(count)+' is not found. '))
			sku_ids = self.env['sku.mapping'].search([('name', '=', sku_id)])
			if sku_ids:
				# print("---------------------------u_sku-------------")
				if not sku_ids.id_number:
					sku_ids.update({'portal_id_type': 'asin', 'id_number': asin})
					# print("---------------------------update--------------")

	def update_products(self):
		prod_pool = self.env['product.product']
		f = base64.b64decode(self.product_file)
		data_file = io.StringIO(f.decode("utf-8"))
		reader = csv.reader(data_file, delimiter=',')
		headers = {}
		for row in reader:
			col_count = 0
			for col in row:
				headers[col] = col_count
				col_count = col_count + 1
			break;
		count =1
		for row in reader:
			default_code = row[headers['Internal Reference']].strip()
			if default_code:
				pro_tmpl_ids = self.env['product.template'].search([('default_code', '=', default_code)])
				# if not pro_tmpl_ids:
				# 	raise UserError(_("Internal Reference "+' in line '+str(count)+' is not found. '))
				categ1 = row[headers['Product Category-1']].strip()
				vals = {}
				categ_id = self.env['product.category'].search([('name', '=', categ1)])
				categ1_id = self.env['product.category1'].search([('name', '=', categ1)])
				if categ_id:
					vals['categ_id'] = categ_id.id
				if categ1_id:
					vals['categ1'] = categ1_id.id
				if not categ_id:
					create_categ_id = self.env['product.category'].create({'name':categ1})
					vals['categ_id'] = create_categ_id.id
				if not categ1_id:
					create_categ1_id = self.env['product.category1'].create({'name':categ1})
					vals['categ1'] = create_categ1_id.id
				pro_tmpl_ids.update(vals)
				count+=1
				print("------------------------count---------------", count)