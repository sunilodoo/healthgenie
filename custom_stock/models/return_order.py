# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from functools import partial
from itertools import groupby
from odoo import api, fields, models, registry, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare
from werkzeug.urls import url_encode
import xmlrpc.client
# url = "http://localhost:8069"
# db = "sinew_fy2122"
# username = "admin"
# password = "admin@0104"


url = "http://192.168.1.4:8081"
db = "healthgenie_new_db_3april2024"
username = "admin"
password = "admin123"

# with registry('sinew_fy2122') as new_cr:
# 	env = api.Environment(new_cr, SUPERUSER_ID, {})
# 	partner = env['res.partner'].search([('name', '=', 'ERP HARBOR CONSULTING SERVICES')], limit=1)
# 	print("----------db-----", partner.name, partner.phone)

class ReturnOrder(models.Model):
	_name = 'return.order'
	_description = 'Return Order'
	# _order = 'sequence'
	# _order = "name desc"
	# _sql_constraints = [
	# ('ord_id_uniq', 'unique(ord_id)', "A Order Id can only be assigned to one Tranfer !")
	# ]
	# name = fields.Char(string="RTO Number")
	name = fields.Char(string="RTO Number", index=True, copy=False, readonly=True, default=lambda self: _('New'))
	return_o_no = fields.Char(string="Return Order No.", required=True)
	return_date = fields.Date(string="Return Date")
	order_date = fields.Datetime(string="Order Date")
	portal_order_id = fields.Char(string="Portal Order ID", required=True)
	odoo_order_b2b = fields.Char(string="Odoo Invoice Number(B2B)")
	odoo_order_b2c = fields.Char(string="Odoo Invoice Number(B2C)")

	partner_name = fields.Char(string="Name(Partner)")
	partner_city = fields.Char(string="City(Partner)")
	state_id = fields.Many2one('res.country.state', string="State(Partner)")
	country_id = fields.Many2one('res.country', string="Country(Partner)")
	partner_zip_code = fields.Char(string="Pin Code(Partner)")
	order_category = fields.Selection([('b2b', 'B2B'), ('b2c', 'B2C')], string="Return Order(B2B/B2C)")
	partner_vat = fields.Char(string="GSTIN(Partner)")
	sale_number = fields.Char(string="Sale Number(B2C)")
	sale_number_b2b = fields.Char(string="Sale Number(B2B)")
	invoice_date = fields.Date(string="Invoice_Date")
	original_order_id = fields.Char(string="Original_Order_id")

	sale_order_id = fields.Many2one('sale.order', string="Odoo Sale Order")
	invoice_order_id = fields.Many2one(related="invoice_line_id.move_id", string="Odoo Invoice Order")
	# invoice_order_id = fields.Many2one('account.move', string="Odoo Invoice Order")

	product_product_id = fields.Many2one("product.product", string="Product Name")
	default_code = fields.Char(string="Product Id")
	asin = fields.Char(string="FSN Number")
	default_code = fields.Char(related="product_product_id.default_code", string="Product Id", store=True)
	# product_product_id = fields.Many2one("product.product", string="Product")
	quntity = fields.Float(string="Quantity")
	from_warehouse_id = fields.Many2one('stock.warehouse', string="Sale From")
	# from_warehouse_id = fields.Many2one('stock.warehouse', string="Sale From", required=True)
	warehouse_id = fields.Many2one('stock.warehouse', string="To Werehouse")
	return_reason = fields.Char(string="Return Reason")
	month_of_return = fields.Selection([
        ('jan', 'January'),
        ('feb', 'February'),
        ('mar', 'March'),
        ('apr', 'April'),
        ('may', 'May'),
        ('jun', 'June'),
        ('jul', 'July'),
        ('aug', 'August'),
        ('sep', 'September'),
        ('oct', 'October'),
        ('nov', 'November'),
        ('dec', 'December')
        ], string="Month of Return", default=False, required=True)
	state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, default='draft')

	invoice_line_id = fields.Many2one('account.move.line', string="Account Invoice Line")
	# inv_line_id_pre_db = fields.Char(string="Previous DB Inv. Line")
	# invoice_line_id = fields.Many2one('account.move.line', string="Account Invoice Line", required=True)
	currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
	price_unit = fields.Float(string='Unit Price', digits='Product Price')
	price_subtotal = fields.Monetary(string='Subtotal', store=True, readonly=True, currency_field='currency_id')
	price_total = fields.Monetary(string='Total', store=True, readonly=True, currency_field='currency_id')
	tax_ids = fields.Many2many(comodel_name='account.tax', store=True, string="Taxes", context={'active_test': False}, check_company=True, help="Taxes that apply on the base amount")
	# tax_ids = fields.Many2many(comodel_name='account.tax', string="Taxes", context={'active_test': False}, check_company=True, help="Taxes that apply on the base amount")
	product_hsn = fields.Char(string="HSN Code.")
	# company_id = fields.Many2one(related='invoice_order_id.company_id', store=True)
	company_id = fields.Many2one('res.company', string="Company", readonly=True, default=lambda self: self.env.company)
	portal_price = fields.Monetary(string="Portal Price")

	shipping_charges = fields.Monetary(string="Shipping Charge")
	gift_wrap_price = fields.Monetary(string="Gift Wrap price")
	item_promo_discount = fields.Monetary(string="Item Promo Discount")

	sgst_rate = fields.Char(string="SGST@")
	sgst_amount = fields.Monetary(string="SGST Amt")
	cgst_rate = fields.Char(string="CGST@")
	cgst_amount = fields.Monetary(string="CGST Amt")
	igst_rate = fields.Char(string="IGST@")
	igst_amount = fields.Monetary(string="IGST Amt")
	tax_sum = fields.Monetary(string="Tax Sum")
	price_tax = fields.Float(string="Price Tax")

	shipping_charges_basic = fields.Monetary(string="Shippng Charge Basic")
	shipping_charges_sgst = fields.Monetary(string="Shippng Charge SGST")
	shipping_charges_cgst = fields.Monetary(string="Shippng Charge CGST")
	shipping_charges_igst = fields.Monetary(string="Shippng Charge IGST")

	gift_wrap_basic = fields.Monetary(string="Gift Wrap Basic")
	gift_wrap_sgst = fields.Monetary(string="Gift Wrap SGST")
	gift_wrap_cgst = fields.Monetary(string="Gift Wrap CGST")
	gift_wrap_igst = fields.Monetary(string="Gift Wrap IGST")

	item_promo_discount_basic = fields.Monetary(string="Item Promo Discount Basic")
	item_promo_sgst = fields.Monetary(string="Item Promo Discount SGST")
	item_promo_cgst = fields.Monetary(string="Item Promo Discount CGST")
	item_promo_igst = fields.Monetary(string="Item Promo Discount IGST")

	subtotal_with_tax = fields.Monetary(string="Subtotal With Tax")
	grand_subtotal = fields.Monetary(string="Grand Subtotal")
	
	# @api.model
	# def create(self, vals):
	# 	res = super(ReturnOrder, self).create(vals)
	# 	vals['name'] = self.env['ir.sequence'].next_by_code('return.order')
	# 	# print("-----------valse----------", vals['name'])
	# 	string1 = vals['name'].split('/')
	# 	# print("-------------1---", string1[0])
	# 	# print("-------------2---", string1[1])
	# 	# print("-------------wh---", self.warehouse_id.code)
	# 	new_seq = string1[0]+'/'+res.warehouse_id.code+'/'+string1[1]
	# 	# print("-----------valse----------", vals['name'])
	# 	res.write({'name': new_seq})
	# 	return res
	def action_confirm(self):
		print("SS::::::::::::::::::::::::::::::::::")
		# rto_ids = self.env['return.order'].search([('state', '=', 'draft')])
		# print("--------after_----_compute_amount--------")
		if self.state == 'draft':
			self._compute_amount()
			if self.name == 'New':
				# if self.order_category == 'b2c':
				self.name = '2324RT/'+str(self.warehouse_id.code)+'/'+str(self.warehouse_id.rto_b2c).zfill(4)
				# self.name = '2223RT/'+str(self.warehouse_id.code)+'/'+str(self.warehouse_id.rto_b2c).zfill(4)
				if self.name:
					wh_so = self.warehouse_id.write({'rto_b2c': self.warehouse_id.rto_b2c+1})
				# if self.order_category == 'b2b':
				# 	print("b2b::::::::::::::::::::::::::")

				self.name = '2324CN/'+str(self.warehouse_id.code)+'/'+str(self.warehouse_id.rto_b2b).zfill(4)
				print("name:::::::::::::::::::::",self.name)
				# self.name = '2223CN/'+str(self.warehouse_id.code)+'/'+str(self.warehouse_id.rto_b2b).zfill(4)
				if self.sale_number_b2b:
					wh_so = self.warehouse_id.write({'rto_b2b': self.warehouse_id.rto_b2b+1})
			self.state = 'done'
			print("--------complete--------")
			# rto.update({'state': 'done'})

	# def action_confirm(self):
	# 	rto_ids = self.env['return.order'].search([('state', '=', 'draft')])
	# 	for rto in rto_ids:
	# 		rto._compute_amount()
	# 		rto.update({'state': 'done'})
	# @api.multi
	# def get_data_from_database(self):
	# 	with registry('sinew_fy2122') as new_cr:
	# 		env = api.Environment(new_cr, SUPERUSER_ID, {})
	# 		partner = env['res.partner'].search([('name', '=', 'ERP HARBOR CONSULTING SERVICES')], limit=1)
	# 		print("----------db-----", partner.name, partner.phone)
	def previous_db_inv_line(self, portal_order_id, default_code):
		common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
		uid = common.authenticate(db, username, password, {})
		models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
		inv_ids = models.execute_kw(db, uid, password, 'account.move', 'search_read', [[['order_id', '=', portal_order_id]]], {'fields': ['partner_id', 'order_category', 'sale_number_b2b', 'sale_number', 'so_id', 'invoice_number_b2b', 'invoice_number', 'invoice_date','warehouse_id', 'is_replacement', 'original_order_id', 'amount_total']})
		inv_line_id = ''
		# print("----------------------------inv_ids--------------", inv_ids)
		if not inv_ids:
		# if not inv_ids:
			raise UserError(_("Original Order ID of "+portal_order_id+" in return order"+self.name+"is not found in previous Database"))
		# if inv_ids:
		if inv_ids[0]:
			# print("----------------------------inv_ids['is_replacement']--------------", inv_ids[0]['is_replacement'])
			# print("----------------------------inv_ids['is_replacement']-----t---------", type(inv_ids[0]['is_replacement']))
			if inv_ids[0]['is_replacement'] == True:
				self.previous_db_inv_line(inv_ids[0]['original_order_id'], default_code)
			elif inv_ids[0]['amount_total'] > 0:
				# print("------------------------partner-before--------------------", inv_ids)
				partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['id', '=', inv_ids[0]['partner_id'][0]]]], {'fields': ['name', 'state_id', 'country_id', 'city', 'zip', 'vat']})
				inv_line_ids = models.execute_kw(db, uid, password, 'account.move.line', 'search_read', [[['move_id', '=', inv_ids[0]['id']], ['sku_name', '=', default_code]]], {'fields': ['product_id', 'tax_ids', 'price_unit', 'product_hsn', 'portal_price', 'shipping_charges', 'gift_wrap_price', 'item_promo_discount']})
				if not inv_line_ids:
					raise UserError(_("Invoice product is not found in privious Database of return order "+self.name+ " as default_code "+default_code))
				else:
					# print("------------------------inv_ids--------------------", inv_ids)
					# print("-------------------------inv_line_ids-------------------", inv_line_ids)
					vals = {
						# 'sale_order_id': inv_ids[0]['so_id'][0],
						# 'invoice_order_id': inv_ids[0]['id'],
						'partner_name': partner_id[0]['name'],
						'partner_city': partner_id[0]['city'],
						'state_id': partner_id[0]['state_id'][0],
						'country_id': partner_id[0]['country_id'][0],
						'partner_zip_code': partner_id[0]['zip'],
						'partner_vat': partner_id[0]['vat'],

						'odoo_order_b2b': inv_ids[0]['invoice_number_b2b'],
						'odoo_order_b2c': inv_ids[0]['invoice_number'],
						'invoice_date': inv_ids[0]['invoice_date'],
						'original_order_id': inv_ids[0]['original_order_id'],

						'order_category': inv_ids[0]['order_category'],
						'sale_number_b2b': inv_ids[0]['sale_number_b2b'],
						'sale_number': inv_ids[0]['sale_number'],
						# 'from_warehouse_id': inv_ids[0]['warehouse_id'][0],
						'from_warehouse_id': self.env['stock.warehouse'].search([('name', '=', inv_ids[0]['warehouse_id'][1])]).id,

						# 'product_product_id': inv_line_ids[0].product_id[0],
						'tax_ids': inv_line_ids[0]['tax_ids'],
						'price_unit': inv_line_ids[0]['price_unit'],
						'product_hsn': inv_line_ids[0]['product_hsn'],
						'portal_price': inv_line_ids[0]['portal_price'],
						'shipping_charges': inv_line_ids[0]['shipping_charges'],
						'gift_wrap_price': inv_line_ids[0]['gift_wrap_price'],
						'item_promo_discount': inv_line_ids[0]['item_promo_discount']
					}
					self.update(vals)
					# print("------------------pre=----------------", portal_order_id, default_code)
			else:
				raise UserError(_("Invoice value must be grater than 0 for original order "+portal_order_id+' in original database'))
	
	def original_order(self, portal_order_id, default_code):
		inv_id = self.env['account.move'].search([('order_id', '=', portal_order_id), ('state', '=', 'posted')])
		inv_id_o_db = ''
		if not inv_id:
			# return 0
			self.previous_db_inv_line(portal_order_id, default_code)
		else:
			if inv_id.is_replacement == True and inv_id.original_order_id:
				self.original_order(inv_id.original_order_id, default_code)
			elif inv_id.amount_total > 0.0:
				invoice_line_id = self.env['account.move.line'].search([('move_id', '=', inv_id.id), ('sku_name', '=', default_code)])
				if not invoice_line_id:
					raise UserError(_("The product of ASIN "+self.asin+' is not in order id '+portal_order_id))
				# return inv_id.id
				self.update({'invoice_line_id': invoice_line_id.id})
			else:
				raise UserError(_("Invoice value must be grater than 0 for "+portal_order_id))

		# print("---------------partner------", inv_ids)
		# print("---------------partner---t---", type(inv_ids))
		# self.sale_order_id = self.invoice_line_id.move_id.so_id.id
		self.invoice_order_id = self.invoice_line_id.move_id.id              #id
		# self.odoo_order_b2b = self.invoice_line_id.move_id.invoice_number_b2b
		# self.odoo_order_b2c = self.invoice_line_id.move_id.invoice_number
		# self.from_warehouse_id = self.invoice_line_id.move_id.warehouse_id.id

		# #------------------------------------------------------------------------------
		# self.product_product_id = self.invoice_line_id.product_id.id
		# # self.tax_ids = [(6, 0, [i.id for i in self.invoice_line_id.tax_ids])]
		# self.tax_ids = self.invoice_line_id.tax_ids
		# # self.tax_ids = self.product_product_id.taxes_id
		# self.price_unit = self.invoice_line_id.price_unit
		# self.product_hsn = self.invoice_line_id.product_hsn
		# self.portal_price = self.invoice_line_id.portal_price
		# self.shipping_charges = self.invoice_line_id.shipping_charges
		# self.gift_wrap_price = self.invoice_line_id.gift_wrap_price
		# self.item_promo_discount = self.invoice_line_id.item_promo_discount


	
	@api.onchange('asin')
	def onchange_asin(self):
		if self.asin:
			p_p_id = self.env['sku.mapping'].search([('id_number', '=', self.asin)])
			if p_p_id:
				self.product_product_id = p_p_id[0].product_id.id
			else:
				raise UserError(_("Product of asin "+self.asin+' is not exists'))

				
	@api.onchange('product_product_id', 'price_unit', 'quntity', 'invoice_line_id')
	# @api.onchange('product_product_id', 'price_unit', 'quntity', 'tax_ids', 'portal_price', 'shipping_charges', 'gift_wrap_price', 'item_promo_discount', 'invoice_line_id')
	# def onchange_compute(self):
	def _compute_amount(self):

		# result = super(SaleOrderLine, self)._compute_amount()
		for line in self:
			# print("-----------------line-------", line)
			# INSERT INTO t(a, b, c) SELECT a, b, c FROM dblink('host=xxx user=xxx password=xxx dbname=xxx', 'SELECT a, b, c FROM t') AS x(a integer, b integer, c integer)
			# SELECT id FROM dblink('dbname=sinew_fy2122', 'SELECT id FROM account_move WHERE id = 499') 
			# ndb = self.env.cr.execute("""SELECT * FROM sinew_fy2122.account_move where id = 400""")
			# print("------------------ndb-----------", self.env.cr.execute("""SELECT id FROM dblink(dbname=sinew_fy2122', 'SELECT id FROM account_move WHERE id = 499')"""))
			# pirnt("------------------ndb-name----------", ndb.name)
			# pirnt("------------------ndb-name----------", ndb.name)
			# self.get_data_from_database()
			# ------------------------------------------------------------------------------
			if line.invoice_line_id:
				# line.product_product_id = line.invoice_line_id.product_id.id
				line.sale_order_id = line.invoice_line_id.move_id.so_id.id
				line.invoice_order_id = line.invoice_line_id.move_id.id
				line.odoo_order_b2b = line.invoice_line_id.move_id.invoice_number_b2b
				line.odoo_order_b2c = line.invoice_line_id.move_id.invoice_number
				line.from_warehouse_id = line.invoice_line_id.move_id.warehouse_id.id
				#------------------------------------------------------------------------------
				# print("----------------GGGGGGGGGGGGGGGGGGGGG_--")
				line.partner_name = line.invoice_line_id.move_id.partner_id.id
				line.partner_city = line.invoice_line_id.move_id.partner_id.city
				line.state_id = line.invoice_line_id.move_id.partner_id.state_id.id
				line.country_id = line.invoice_line_id.move_id.partner_id.country_id.id
				line.partner_zip_code = line.invoice_line_id.move_id.partner_id.zip
				line.partner_vat = line.invoice_line_id.move_id.partner_id.vat
				line.order_category = line.invoice_line_id.move_id.order_category
				line.sale_number_b2b = line.invoice_line_id.move_id.sale_number_b2b
				line.sale_number = line.invoice_line_id.move_id.sale_number
				# self.tax_ids = [(6, 0, [i.id for i in self.invoice_line_id.tax_ids])]
				line.tax_ids = line.invoice_line_id.tax_ids
				# self.tax_ids = self.product_product_id.taxes_id
				line.price_unit = line.invoice_line_id.price_unit
				line.product_hsn = line.invoice_line_id.product_hsn
				line.portal_price = line.invoice_line_id.portal_price
				line.shipping_charges = line.invoice_line_id.shipping_charges
				line.gift_wrap_price = line.invoice_line_id.gift_wrap_price
				line.item_promo_discount = line.invoice_line_id.item_promo_discount
			if line.portal_order_id and line.default_code:
				if not line.invoice_line_id:
					line.original_order(line.portal_order_id, line.default_code)
			# print("-----------portal_price-----", self.invoice_line_id.portal_price)
			# print("-----------portal_price---ttttt--", type(self.invoice_line_id.portal_price))
			# print("-----------tax_ids-----", self.tax_ids)
			for tax in line.tax_ids:
				# print("----------tax-------", tax)
				if line.invoice_order_id:
					if line.invoice_order_id.order_category == 'b2b':
						# print("---------------------line.invoice_order_id-----------", line.invoice_order_id)
						# print("---------------------b2b-----------",)
						p_gstin = line.invoice_order_id.partner_id.vat
						w_gstin = line.invoice_order_id.warehouse_id.gstin
						p_gstin_s_c = p_gstin[0]+p_gstin[1]
						w_gstin_s_c = w_gstin[0]+w_gstin[1]
						# print("---------------------p_gstin_s_c-----------", p_gstin_s_c)
						# print("---------------------w_gstin_s_c-----------", w_gstin_s_c)
						if p_gstin_s_c == w_gstin_s_c:
							tax_rate = tax.children_tax_ids[0].amount
							tax_percentage = 2*tax_rate
							tax_amount = round((tax_percentage*line.portal_price/(100+tax_percentage))/2, 2)
							tax_amount_total = tax_amount*line.quntity
							price_unit = line.portal_price - 2*tax_amount
							price_subtotal = price_unit*line.quntity
							shipping_tax = 0.0
							shipping_charges_basic = 0.0
							if line.shipping_charges>0:
								shipping_tax = round((line.shipping_charges*tax_percentage/(100+tax_percentage))/2, 2)
								shipping_charges_basic = line.shipping_charges - 2*shipping_tax
							gift_tax = 0.0
							gift_wrap_basic = 0.0
							if line.gift_wrap_price>0:
								gift_tax = round((line.gift_wrap_price*tax_percentage/(100+tax_percentage))/2, 2)
								gift_wrap_basic = line.gift_wrap_price - 2*gift_tax
							promo_tax = 0.0
							item_promo_discount_basic = 0.0
							if line.item_promo_discount>0:
								promo_tax = round((line.item_promo_discount*tax_percentage/(100+tax_percentage))/2, 2)
								item_promo_discount_basic = line.item_promo_discount - 2*promo_tax

							line.update({
								'price_unit': price_unit,
								'price_subtotal': price_subtotal,
								'price_tax': 2*tax_amount_total,
								'sgst_rate': tax.children_tax_ids[0].name,
								'sgst_amount': tax_amount_total,
								'cgst_rate': tax.children_tax_ids[1].name,
								'cgst_amount': tax_amount_total,
								'igst_rate': '',
								'igst_amount': 0.0,
								'tax_sum': tax_percentage,
								'subtotal_with_tax': line.portal_price*line.quntity,

								'shipping_charges_basic': shipping_charges_basic,
								'shipping_charges_sgst': shipping_tax,
								'shipping_charges_cgst': shipping_tax,
								'shipping_charges_igst': 0.0,

								'gift_wrap_basic': gift_wrap_basic,
								'gift_wrap_sgst': gift_tax,
								'gift_wrap_cgst': gift_tax,
								'gift_wrap_igst': 0.0,

								'item_promo_discount_basic': item_promo_discount_basic,
								'item_promo_sgst': promo_tax,
								'item_promo_cgst': promo_tax,
								'item_promo_igst': 0.0,

								'grand_subtotal': line.portal_price*line.quntity + line.shipping_charges+line.gift_wrap_price-line.item_promo_discount
							})
						else:
							tax_rate = tax.children_tax_ids[0].amount
							tax_percentage = 2*tax_rate
							tax_amount = round(tax_percentage*line.portal_price/(100+tax_percentage), 2)
							tax_amount_total = tax_amount*line.quntity
							price_unit = line.portal_price - tax_amount	
							price_subtotal = price_unit*line.quntity

							shipping_tax = 0.0
							shipping_charges_basic = 0.0
							if line.shipping_charges>0:
								shipping_tax = round(line.shipping_charges*tax_percentage/(100+tax_percentage), 2)
								shipping_charges_basic = line.shipping_charges - shipping_tax

							gift_tax = 0.0
							gift_wrap_basic = 0.0
							if line.gift_wrap_price>0:
								gift_tax = round(line.gift_wrap_price*tax_percentage/(100+tax_percentage), 2)
								gift_wrap_basic = line.gift_wrap_price - gift_tax

							promo_tax = 0.0
							item_promo_discount_basic = 0.0
							if line.item_promo_discount>0:
								promo_tax = round(line.item_promo_discount*tax_percentage/(100+tax_percentage), 2)
								item_promo_discount_basic = line.item_promo_discount - promo_tax

							line.update({
								'price_unit': line.portal_price - tax_amount,
								'price_subtotal': price_subtotal,
								'price_tax': tax_amount_total,
								'sgst_rate': '',
								'sgst_amount': 0.0,
								'cgst_rate': '',
								'cgst_amount': 0.0,
								'igst_rate': 'IGST'+str(tax_percentage)+'%',
								# 'igst_rate': 'IGST'+str(2*float(tax.children_tax_ids[0].amount))+'%',
								'igst_amount': tax_amount_total,
								'tax_sum': tax_percentage,
								'subtotal_with_tax': line.portal_price*line.quntity,

								'shipping_charges_basic': shipping_charges_basic,
								'shipping_charges_sgst': 0.0,
								'shipping_charges_cgst': 0.0,
								'shipping_charges_igst': shipping_tax,

								'gift_wrap_basic': gift_wrap_basic,
								'gift_wrap_sgst': 0.0,
								'gift_wrap_cgst': 0.0,
								'gift_wrap_igst': gift_tax,

								'item_promo_discount_basic': item_promo_discount_basic,
								'item_promo_sgst': 0.0,
								'item_promo_cgst': 0.0,
								'item_promo_igst': promo_tax,

								'grand_subtotal': line.portal_price*line.quntity + line.shipping_charges+line.gift_wrap_price-line.item_promo_discount
							})
					else:
						# print("---------------------line.invoice_order_id-----------", line.invoice_order_id)
						# print("---------------------b2c-----------",)
						if line.invoice_order_id.partner_id.state_id.name == line.invoice_order_id.warehouse_id.state_id.name:
							tax_rate = tax.children_tax_ids[0].amount
							tax_percentage = 2*tax_rate
							tax_amount = round((tax_percentage*line.portal_price/(100+tax_percentage))/2, 2)
							tax_amount_total = tax_amount*line.quntity
							price_unit = line.portal_price - 2*tax_amount
							price_subtotal = price_unit*line.quntity
							shipping_tax = 0.0
							shipping_charges_basic = 0.0
							if line.shipping_charges>0:
								shipping_tax = round((line.shipping_charges*tax_percentage/(100+tax_percentage))/2, 2)
								shipping_charges_basic = line.shipping_charges - 2*shipping_tax
							gift_tax = 0.0
							gift_wrap_basic = 0.0
							if line.gift_wrap_price>0:
								gift_tax = round((line.gift_wrap_price*tax_percentage/(100+tax_percentage))/2, 2)
								gift_wrap_basic = line.gift_wrap_price - 2*gift_tax
							promo_tax = 0.0
							item_promo_discount_basic = 0.0
							if line.item_promo_discount>0:
								promo_tax = round((line.item_promo_discount*tax_percentage/(100+tax_percentage))/2, 2)
								item_promo_discount_basic = line.item_promo_discount - 2*promo_tax

							line.update({
								'price_unit': price_unit,
								'price_subtotal': price_subtotal,
								'price_tax': 2*tax_amount_total,
								'sgst_rate': tax.children_tax_ids[0].name,
								'sgst_amount': tax_amount_total,
								'cgst_rate': tax.children_tax_ids[1].name,
								'cgst_amount': tax_amount_total,
								'igst_rate': '',
								'igst_amount': 0.0,
								'tax_sum': tax_percentage,
								'subtotal_with_tax': line.portal_price*line.quntity,

								'shipping_charges_basic': shipping_charges_basic,
								'shipping_charges_sgst': shipping_tax,
								'shipping_charges_cgst': shipping_tax,
								'shipping_charges_igst': 0.0,

								'gift_wrap_basic': gift_wrap_basic,
								'gift_wrap_sgst': gift_tax,
								'gift_wrap_cgst': gift_tax,
								'gift_wrap_igst': 0.0,

								'item_promo_discount_basic': item_promo_discount_basic,
								'item_promo_sgst': promo_tax,
								'item_promo_cgst': promo_tax,
								'item_promo_igst': 0.0,

								'grand_subtotal': line.portal_price*line.quntity + line.shipping_charges+line.gift_wrap_price-line.item_promo_discount
							})
						else:
							tax_rate = tax.children_tax_ids[0].amount
							tax_percentage = 2*tax_rate
							tax_amount = round(tax_percentage*line.portal_price/(100+tax_percentage), 2)
							tax_amount_total = tax_amount*line.quntity
							price_unit = line.portal_price - tax_amount	
							price_subtotal = price_unit*line.quntity

							shipping_tax = 0.0
							shipping_charges_basic = 0.0
							if line.shipping_charges>0:
								shipping_tax = round(line.shipping_charges*tax_percentage/(100+tax_percentage), 2)
								shipping_charges_basic = line.shipping_charges - shipping_tax

							gift_tax = 0.0
							gift_wrap_basic = 0.0
							if line.gift_wrap_price>0:
								gift_tax = round(line.gift_wrap_price*tax_percentage/(100+tax_percentage), 2)
								gift_wrap_basic = line.gift_wrap_price - gift_tax

							promo_tax = 0.0
							item_promo_discount_basic = 0.0
							if line.item_promo_discount>0:
								promo_tax = round(line.item_promo_discount*tax_percentage/(100+tax_percentage), 2)
								item_promo_discount_basic = line.item_promo_discount - promo_tax

							line.update({
								'price_unit': line.portal_price - tax_amount,
								'price_subtotal': price_subtotal,
								'price_tax': tax_amount_total,
								'sgst_rate': '',
								'sgst_amount': 0.0,
								'cgst_rate': '',
								'cgst_amount': 0.0,
								'igst_rate': 'IGST'+str(tax_percentage)+'%',
								# 'igst_rate': 'IGST'+str(2*float(tax.children_tax_ids[0].amount))+'%',
								'igst_amount': tax_amount_total,
								'tax_sum': tax_percentage,
								'subtotal_with_tax': line.portal_price*line.quntity,

								'shipping_charges_basic': shipping_charges_basic,
								'shipping_charges_sgst': 0.0,
								'shipping_charges_cgst': 0.0,
								'shipping_charges_igst': shipping_tax,

								'gift_wrap_basic': gift_wrap_basic,
								'gift_wrap_sgst': 0.0,
								'gift_wrap_cgst': 0.0,
								'gift_wrap_igst': gift_tax,

								'item_promo_discount_basic': item_promo_discount_basic,
								'item_promo_sgst': 0.0,
								'item_promo_cgst': 0.0,
								'item_promo_igst': promo_tax,

								'grand_subtotal': line.portal_price*line.quntity + line.shipping_charges+line.gift_wrap_price-line.item_promo_discount
							})
				else:
					if line.order_category == 'b2b':
						# print("---------------------line.order_category-----------", line.order_category)
						# print("-----------------2----b2b-----------",)
						# print("---------------------b2b-----------",)
						p_gstin = line.partner_vat
						w_gstin = line.from_warehouse_id.gstin
						p_gstin_s_c = p_gstin[0]+p_gstin[1]
						w_gstin_s_c = w_gstin[0]+w_gstin[1]
						# print("---------------------p_gstin_s_c-----------", p_gstin_s_c)
						# print("---------------------w_gstin_s_c-----------", w_gstin_s_c)
						if p_gstin_s_c == w_gstin_s_c:
							tax_rate = tax.children_tax_ids[0].amount
							tax_percentage = 2*tax_rate
							tax_amount = round((tax_percentage*line.portal_price/(100+tax_percentage))/2, 2)
							tax_amount_total = tax_amount*line.quntity
							price_unit = line.portal_price - 2*tax_amount
							price_subtotal = price_unit*line.quntity
							shipping_tax = 0.0
							shipping_charges_basic = 0.0
							if line.shipping_charges>0:
								shipping_tax = round((line.shipping_charges*tax_percentage/(100+tax_percentage))/2, 2)
								shipping_charges_basic = line.shipping_charges - 2*shipping_tax
							gift_tax = 0.0
							gift_wrap_basic = 0.0
							if line.gift_wrap_price>0:
								gift_tax = round((line.gift_wrap_price*tax_percentage/(100+tax_percentage))/2, 2)
								gift_wrap_basic = line.gift_wrap_price - 2*gift_tax
							promo_tax = 0.0
							item_promo_discount_basic = 0.0
							if line.item_promo_discount>0:
								promo_tax = round((line.item_promo_discount*tax_percentage/(100+tax_percentage))/2, 2)
								item_promo_discount_basic = line.item_promo_discount - 2*promo_tax

							line.update({
								'price_unit': price_unit,
								'price_subtotal': price_subtotal,
								'price_tax': 2*tax_amount_total,
								'sgst_rate': tax.children_tax_ids[0].name,
								'sgst_amount': tax_amount_total,
								'cgst_rate': tax.children_tax_ids[1].name,
								'cgst_amount': tax_amount_total,
								'igst_rate': '',
								'igst_amount': 0.0,
								'tax_sum': tax_percentage,
								'subtotal_with_tax': line.portal_price*line.quntity,

								'shipping_charges_basic': shipping_charges_basic,
								'shipping_charges_sgst': shipping_tax,
								'shipping_charges_cgst': shipping_tax,
								'shipping_charges_igst': 0.0,

								'gift_wrap_basic': gift_wrap_basic,
								'gift_wrap_sgst': gift_tax,
								'gift_wrap_cgst': gift_tax,
								'gift_wrap_igst': 0.0,

								'item_promo_discount_basic': item_promo_discount_basic,
								'item_promo_sgst': promo_tax,
								'item_promo_cgst': promo_tax,
								'item_promo_igst': 0.0,

								'grand_subtotal': line.portal_price*line.quntity + line.shipping_charges+line.gift_wrap_price-line.item_promo_discount
							})
						else:
							tax_rate = tax.children_tax_ids[0].amount
							tax_percentage = 2*tax_rate
							tax_amount = round(tax_percentage*line.portal_price/(100+tax_percentage), 2)
							tax_amount_total = tax_amount*line.quntity
							price_unit = line.portal_price - tax_amount	
							price_subtotal = price_unit*line.quntity

							shipping_tax = 0.0
							shipping_charges_basic = 0.0
							if line.shipping_charges>0:
								shipping_tax = round(line.shipping_charges*tax_percentage/(100+tax_percentage), 2)
								shipping_charges_basic = line.shipping_charges - shipping_tax

							gift_tax = 0.0
							gift_wrap_basic = 0.0
							
							if line.gift_wrap_price>0:
								gift_tax = round(line.gift_wrap_price*tax_percentage/(100+tax_percentage), 2)
								gift_wrap_basic = line.gift_wrap_price - gift_tax

							promo_tax = 0.0
							item_promo_discount_basic = 0.0
							if line.item_promo_discount>0:
								promo_tax = round(line.item_promo_discount*tax_percentage/(100+tax_percentage), 2)
								item_promo_discount_basic = line.item_promo_discount - promo_tax

							line.update({
								'price_unit': line.portal_price - tax_amount,
								'price_subtotal': price_subtotal,
								'price_tax': tax_amount_total,
								'sgst_rate': '',
								'sgst_amount': 0.0,
								'cgst_rate': '',
								'cgst_amount': 0.0,
								'igst_rate': 'IGST'+str(tax_percentage)+'%',
								# 'igst_rate': 'IGST'+str(2*float(tax.children_tax_ids[0].amount))+'%',
								'igst_amount': tax_amount_total,
								'tax_sum': tax_percentage,
								'subtotal_with_tax': line.portal_price*line.quntity,

								'shipping_charges_basic': shipping_charges_basic,
								'shipping_charges_sgst': 0.0,
								'shipping_charges_cgst': 0.0,
								'shipping_charges_igst': shipping_tax,

								'gift_wrap_basic': gift_wrap_basic,
								'gift_wrap_sgst': 0.0,
								'gift_wrap_cgst': 0.0,
								'gift_wrap_igst': gift_tax,

								'item_promo_discount_basic': item_promo_discount_basic,
								'item_promo_sgst': 0.0,
								'item_promo_cgst': 0.0,
								'item_promo_igst': promo_tax,

								'grand_subtotal': line.portal_price*line.quntity + line.shipping_charges+line.gift_wrap_price-line.item_promo_discount
							})
					else:
						# print("---------------------line.order_category-----------", line.order_category)
						# print("-----------------2----b2c-----------",)
						if line.state_id.id == line.from_warehouse_id.state_id.id:
							tax_rate = tax.children_tax_ids[0].amount
							tax_percentage = 2*tax_rate
							tax_amount = round((tax_percentage*line.portal_price/(100+tax_percentage))/2, 2)
							tax_amount_total = tax_amount*line.quntity
							price_unit = line.portal_price - 2*tax_amount
							price_subtotal = price_unit*line.quntity
							shipping_tax = 0.0
							shipping_charges_basic = 0.0
							if line.shipping_charges>0:
								shipping_tax = round((line.shipping_charges*tax_percentage/(100+tax_percentage))/2, 2)
								shipping_charges_basic = line.shipping_charges - 2*shipping_tax
							gift_tax = 0.0
							gift_wrap_basic = 0.0
							if line.gift_wrap_price>0:
								gift_tax = round((line.gift_wrap_price*tax_percentage/(100+tax_percentage))/2, 2)
								gift_wrap_basic = line.gift_wrap_price - 2*gift_tax
							promo_tax = 0.0
							item_promo_discount_basic = 0.0
							if line.item_promo_discount>0:
								promo_tax = round((line.item_promo_discount*tax_percentage/(100+tax_percentage))/2, 2)
								item_promo_discount_basic = line.item_promo_discount - 2*promo_tax

							line.update({
								'price_unit': price_unit,
								'price_subtotal': price_subtotal,
								'price_tax': 2*tax_amount_total,
								'sgst_rate': tax.children_tax_ids[0].name,
								'sgst_amount': tax_amount_total,
								'cgst_rate': tax.children_tax_ids[1].name,
								'cgst_amount': tax_amount_total,
								'igst_rate': '',
								'igst_amount': 0.0,
								'tax_sum': tax_percentage,
								'subtotal_with_tax': line.portal_price*line.quntity,

								'shipping_charges_basic': shipping_charges_basic,
								'shipping_charges_sgst': shipping_tax,
								'shipping_charges_cgst': shipping_tax,
								'shipping_charges_igst': 0.0,

								'gift_wrap_basic': gift_wrap_basic,
								'gift_wrap_sgst': gift_tax,
								'gift_wrap_cgst': gift_tax,
								'gift_wrap_igst': 0.0,

								'item_promo_discount_basic': item_promo_discount_basic,
								'item_promo_sgst': promo_tax,
								'item_promo_cgst': promo_tax,
								'item_promo_igst': 0.0,

								'grand_subtotal': line.portal_price*line.quntity + line.shipping_charges+line.gift_wrap_price-line.item_promo_discount
							})
						else:
							tax_rate = tax.children_tax_ids[0].amount
							tax_percentage = 2*tax_rate
							tax_amount = round(tax_percentage*line.portal_price/(100+tax_percentage), 2)
							tax_amount_total = tax_amount*line.quntity
							price_unit = line.portal_price - tax_amount	
							price_subtotal = price_unit*line.quntity

							shipping_tax = 0.0
							shipping_charges_basic = 0.0
							if line.shipping_charges>0:
								shipping_tax = round(line.shipping_charges*tax_percentage/(100+tax_percentage), 2)
								shipping_charges_basic = line.shipping_charges - shipping_tax

							gift_tax = 0.0
							gift_wrap_basic = 0.0
							if line.gift_wrap_price>0:
								gift_tax = round(line.gift_wrap_price*tax_percentage/(100+tax_percentage), 2)
								gift_wrap_basic = line.gift_wrap_price - gift_tax

							promo_tax = 0.0
							item_promo_discount_basic = 0.0
							if line.item_promo_discount>0:
								promo_tax = round(line.item_promo_discount*tax_percentage/(100+tax_percentage), 2)
								item_promo_discount_basic = line.item_promo_discount - promo_tax

							line.update({
								'price_unit': line.portal_price - tax_amount,
								'price_subtotal': price_subtotal,
								'price_tax': tax_amount_total,
								'sgst_rate': '',
								'sgst_amount': 0.0,
								'cgst_rate': '',
								'cgst_amount': 0.0,
								'igst_rate': 'IGST'+str(tax_percentage)+'%',
								# 'igst_rate': 'IGST'+str(2*float(tax.children_tax_ids[0].amount))+'%',
								'igst_amount': tax_amount_total,
								'tax_sum': tax_percentage,
								'subtotal_with_tax': line.portal_price*line.quntity,

								'shipping_charges_basic': shipping_charges_basic,
								'shipping_charges_sgst': 0.0,
								'shipping_charges_cgst': 0.0,
								'shipping_charges_igst': shipping_tax,

								'gift_wrap_basic': gift_wrap_basic,
								'gift_wrap_sgst': 0.0,
								'gift_wrap_cgst': 0.0,
								'gift_wrap_igst': gift_tax,

								'item_promo_discount_basic': item_promo_discount_basic,
								'item_promo_sgst': 0.0,
								'item_promo_cgst': 0.0,
								'item_promo_igst': promo_tax,

								'grand_subtotal': line.portal_price*line.quntity + line.shipping_charges+line.gift_wrap_price-line.item_promo_discount
							})
		# return result





