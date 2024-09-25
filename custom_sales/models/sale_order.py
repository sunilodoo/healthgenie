# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
import num2words
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import Warning, UserError
#from openerp import netsvc

class SaleOrder(models.Model):
	_inherit = 'sale.order'
	_order = 'sequence'
	_order = "name desc"
	_sql_constraints = [
	('order_id', 'unique(order_id)', "Portal order Id Must be unique !")
	]

	sale_number = fields.Char(string="Sale Number", copy=False)
	# sale_number_b2b = fields.Char(string="Sale Number(B2B)", copy=False)
	order_id = fields.Char(string=" Portal Order ID")
	is_replacement = fields.Boolean(string="Is Replacement", default=False)
	original_order_id = fields.Char(string="Original Order ID")
	order_type = fields.Char(string="Order Type")
	order_date = fields.Date(string="Order Date(Portal)")
	invoice_no = fields.Char(string="Invoice No.")
	invoice_date = fields.Date(string="Invoice Date")
	month_of_sale = fields.Selection([
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
		], string="Month of sale", default=False, required=True)
	portal_id = fields.Many2one('res.portal', string="Portal")
	# third_party = fields.Many2one('res.partner', string="Third Party")
	# order_category = fields.Selection([('b2b', 'B2B'), ('b2c', 'B2C')], string="Order(B2B/B2C)", required=True)
	# tracking_no = fields.Char(string="Tracking No.")
	# delivery_partner_name = fields.Char(string="Delivery Partner Name")
	# hg_party_id = fields.Char(string="HG Party ID")
	sgst = fields.Monetary(string="SGST", store=True)
	cgst = fields.Monetary(string="CGST", store=True)
	igst = fields.Monetary(string="IGST", store=True)

	total_s_c = fields.Monetary(string="Shipping Charge")
	total_s_c_untaxed = fields.Monetary(string="Total Shipping Untaxed")
	total_s_c_tax = fields.Monetary(string="Total Shipping Tax")

	c_amount_untaxed = fields.Monetary(string="Untaxed Amount")
	return_payment = fields.Char(string="Return Payment")
	payment_recieved = fields.Char(string="Payment Received")
	short_access_recieved = fields.Char(string="Short And Access Recieved")
	sale_payment_ids = fields.One2many('sale.payment', 'order_id', string='Sale_payment')

	# total_s_c_basic = fields.Monetary(string="Shipping Charge Basic")
	# total_s_c_sgst = fields.Monetary(string="Shipping Charge SGST")
	# total_s_c_cgst = fields.Monetary(string="Shipping Charge CGST")
	# total_s_c_igst = fields.Monetary(string="Shipping Charge IGST")

	# Change By Keshav
	def action_confirm(self):
		res = super(SaleOrder, self).action_confirm()
		# if self.order_category == 'b2c':
		if not self.sale_number:
			if self.portal_id.name:
				self.sale_number = '24-25'+'/'+str(self.warehouse_id.inv_code)+'/'+str(self.warehouse_id.next_number_so_f).zfill(7)
				# self.sale_number = '22-23'+'/'+str(self.warehouse_id.inv_code)+'/'+str(self.warehouse_id.next_number_so_f).zfill(7)
				if self.sale_number:
					wh_so = self.warehouse_id.write({'next_number_so_f': self.warehouse_id.next_number_so_f+1})
			# else:
			# 	self.sale_number = '24-25'+'/HI/'+str(self.warehouse_id.next_number_so_o).zfill(7)
			# 	# self.sale_number = '22-23'+'/HI/'+str(self.warehouse_id.next_number_so_o).zfill(7)
			# 	if self.sale_number:
			# 		wh_so = self.warehouse_id.write({'next_number_so_o': self.warehouse_id.next_number_so_o+1})
		# if self.order_category == 'b2b':
		# 	if not self.sale_number_b2b:
		# 		self.sale_number_b2b = '2122'+'B'+'/'+str(self.warehouse_id.code)+'/'+str(self.warehouse_id.next_number_so_b2b).zfill(5)
		# 		if self.sale_number_b2b:
		# 			wh_so = self.warehouse_id.write({'next_number_so_b2b': self.warehouse_id.next_number_so_b2b+1})
		# return False
	@api.depends('order_line.price_total')
	def _amount_all(self):
		for order in self:
			amount_untaxed = amount_tax = 0.0
			sgst = 0.0
			cgst = 0.0
			igst = 0.0

			total_s_c = 0.0
			grand_subtotal = 0.0

			total_s_c_untaxed = 0.0
			total_s_c_tax = 0.0
			c_amount_untaxed = 0.0

			for line in order.order_line:
				amount_untaxed += line.price_subtotal
				amount_tax += line.price_tax
				sgst += line.sgst_amount
				cgst += line.cgst_amount
				igst += line.igst_amount

				total_s_c_untaxed += line.shipping_charges_untaxed
				total_s_c_tax += line.shipping_charges_tax
				c_amount_untaxed += line.c_price_subtotal

				total_s_c += line.shipping_charges
				grand_subtotal += line.grand_subtotal

			order.update({
				'amount_untaxed': amount_untaxed,
				'amount_tax': amount_tax,
				'sgst': sgst,
				'cgst': cgst,
				'igst': igst,

				'total_s_c': total_s_c,
				'total_s_c_untaxed': total_s_c_untaxed,
				'total_s_c_tax': total_s_c_tax,
				'c_amount_untaxed': c_amount_untaxed,
				# 'total_s_c_basic': total_s_c_basic,
				'amount_total': round(grand_subtotal, 2)
				# 'amount_total': round(amount_untaxed+sgst+cgst+igst+grand_subtotal)
				# 'sgst': sgst if order.partner_id.state_id.name == order.warehouse_id.state_id.name else 0.0,
				# 'cgst': cgst if order.partner_id.state_id.name == order.warehouse_id.state_id.name else 0.0,
				# 'igst': igst if order.partner_id.state_id.name != order.warehouse_id.state_id.name else 0.0,
			})

	def _prepare_invoice(self):
		# print("-------------custom _prepare_invoice--")
		res = super(SaleOrder, self)._prepare_invoice()
		res['so_id'] = self.id
		res['sale_number'] = self.sale_number
		# res['sale_number_b2b'] = self.sale_number_b2b
		res['order_type'] = self.order_type
		res['order_date'] = self.order_date
		res['warehouse_id'] = self.warehouse_id.id
		res['order_id'] = self.order_id
		res['is_replacement'] = self.is_replacement
		res['original_order_id'] = self.original_order_id
		res['invoice_no'] = self.invoice_no
		# res['order_category'] = self.order_category
		res['sgst'] = self.sgst
		res['cgst'] = self.cgst
		res['igst'] = self.igst
		res['invoice_date'] = self.invoice_date
		res['month_of_sale'] = self.month_of_sale
		res['portal_id'] = self.portal_id.id

		res['total_s_c'] = self.total_s_c
		res['amount_total'] = self.amount_total

		res['total_s_c_untaxed'] = self.total_s_c_untaxed
		res['total_s_c_tax'] = self.total_s_c_tax
		res['c_amount_untaxed'] = self.c_amount_untaxed
		# print("-------------custom res--", res)
		return res
	@api.onchange('warehouse_id')
	def _onchange_warehouse_id(self):
		for line in self.order_line:
			line._compute_amount()
			# line.env['sale.order.line'].search([('id', '=', self.id)])._compute_amount()


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	product_hsn = fields.Char(related='product_id.product_tmpl_id.l10n_in_hsn_code', string="HSN Code.")
	product_default_code = fields.Char(related='product_id.product_tmpl_id.default_code', string="Product ID.", store=True)
	sku_id = fields.Many2one('sku.mapping', string="SKU ID")
	sku_name = fields.Char(string="SKU ID Name")
	portal_price = fields.Monetary(string="Portal Price")
	sgst_rate = fields.Char(string="SGST@")
	shipping_charges_untaxed = fields.Monetary(string="Shipping Charge Untaxed", store=True)
	shipping_charges_tax = fields.Monetary(string="Shipping Charge Tax", store=True)
	shipping_charges = fields.Monetary(string="Shipping Charges", store=True)
	# gift_wrap_price = fields.Monetary(string="Gift Wrap price")
	# item_promo_discount = fields.Monetary(string="Item Promo Discount")

	sgst_rate = fields.Char(string="SGST@")
	sgst_amount = fields.Monetary(string="SGST Amt")
	cgst_rate = fields.Char(string="CGST@")
	cgst_amount = fields.Monetary(string="CGST Amt")
	igst_rate = fields.Char(string="IGST@")
	igst_amount = fields.Monetary(string="IGST Amt")
	tax_sum = fields.Monetary(string="Tax Sum")
	c_price_subtotal = fields.Monetary(string="Subtotal", store=True)

	# shipping_charges_basic = fields.Monetary(string="Shippng Charge Basic")
	# shipping_charges_sgst = fields.Monetary(string="Shippng Charge SGST")
	# shipping_charges_cgst = fields.Monetary(string="Shippng Charge CGST")
	# shipping_charges_igst = fields.Monetary(string="Shippng Charge IGST")

	# gift_wrap_basic = fields.Monetary(string="Gift Wrap Basic")
	# gift_wrap_sgst = fields.Monetary(string="Gift Wrap SGST")
	# gift_wrap_cgst = fields.Monetary(string="Gift Wrap CGST")
	# gift_wrap_igst = fields.Monetary(string="Gift Wrap IGST")

	# item_promo_discount_basic = fields.Monetary(string="Item Promo Discount Basic")
	# item_promo_sgst = fields.Monetary(string="Item Promo Discount SGST")
	# item_promo_cgst = fields.Monetary(string="Item Promo Discount CGST")
	# item_promo_igst = fields.Monetary(string="Item Promo Discount IGST")

	subtotal_with_tax = fields.Monetary(string="Subtotal With Tax")
	grand_subtotal = fields.Monetary(string="Grand Subtotal")
	# comp_calc = fields.Monetary(string="Only", compute='only_fucntion')

	@api.onchange('product_id')
	def product_id_change_sku(self):
		# if self.product_id.sku_line_id:
		# 	self.sku_id = self.product_id.sku_line_id[0].name
		# else:
		self.sku_name = self.product_id.default_code
		# self.sku_id = self.product_id.sku_id if self.product_id.sku_id else ''

	@api.onchange('sku_id')
	def sku_id_change(self):
		self.product_id = self.sku_id.product_id
	def _prepare_invoice_line(self, **optional_values):
		res = super(SaleOrderLine, self)._prepare_invoice_line()
		res['product_hsn'] = self.product_hsn
		res['sku_name'] = self.sku_name
		res['portal_price'] = self.portal_price
		res['shipping_charges_untaxed'] = self.shipping_charges_untaxed
		res['shipping_charges_tax'] = self.shipping_charges_tax
		res['shipping_charges'] = self.shipping_charges
		res['sgst_rate'] = self.sgst_rate
		res['sgst_amount'] = self.sgst_amount
		res['cgst_rate'] = self.cgst_rate
		res['cgst_amount'] = self.cgst_amount
		res['igst_rate'] = self.igst_rate
		res['igst_amount'] = self.igst_amount
		res['tax_sum'] = self.tax_sum
		res['price_tax'] = self.price_tax
		res['price_subtotal'] = self.price_subtotal
		res['c_price_subtotal'] = self.c_price_subtotal

		# res['shipping_charges_basic'] = self.shipping_charges_basic
		# res['shipping_charges_sgst'] = self.shipping_charges_sgst
		# res['shipping_charges_cgst'] = self.shipping_charges_cgst
		# res['shipping_charges_igst'] = self.shipping_charges_igst
		# res['gift_wrap_basic'] = self.gift_wrap_basic
		# res['gift_wrap_sgst'] = self.gift_wrap_sgst
		# res['gift_wrap_cgst'] = self.gift_wrap_cgst
		# res['gift_wrap_igst'] = self.gift_wrap_igst
		# res['item_promo_discount_basic'] = self.item_promo_discount_basic
		# res['item_promo_sgst'] = self.item_promo_sgst
		# res['item_promo_cgst'] = self.item_promo_cgst
		# res['item_promo_igst'] = self.item_promo_igst

		res['subtotal_with_tax'] = self.subtotal_with_tax
		res['grand_subtotal'] = self.grand_subtotal
		# print("-------------_prepare_invoice_line--")
		return res
		# self.ensure_one()
		# print("-----------------self.tax_id.ids--------", self.tax_id.ids)
		# res = {
		# 	'display_type': self.display_type,
		# 	'sequence': self.sequence,
		# 	'name': self.name,
		# 	'product_id': self.product_id.id,
		# 	'product_uom_id': self.product_uom.id,
		# 	'quantity': self.qty_to_invoice,
		# 	'discount': self.discount,
		# 	'price_unit': self.price_unit,
		# 	'tax_ids': [(6, 0, self.tax_id.ids)],
		# 	'analytic_account_id': self.order_id.analytic_account_id.id,
		# 	'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
		# 	'sale_line_ids': [(4, self.id)],
		# }
		# if optional_values:
		# 	res.update(optional_values)
		# if self.display_type:
		# 	res['account_id'] = False
		# return res

	# @api.model_create_multi
	# def create(self, vals_list):
	# 	result = super(SaleOrderLine, self).create(vals_list)
	# 	print("--------print @@@------------")
	# 	self._compute_amount()
	# 	return result
	# @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
 #    def _compute_amount(self):
 #        """
 #        Compute the amounts of the SO line.
 #        """
 #        for line in self:
 #            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
 #            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
 #            line.update({
 #                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
 #                'price_total': taxes['total_included'],
 #                'price_subtotal': taxes['total_excluded'],
 #            })
 #            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
 #                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
	@api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id', 'portal_price', 'shipping_charges')
	# def onchange_compute(self):
	def _compute_amount(self):
		result = super(SaleOrderLine, self)._compute_amount()
		for line in self:
			print("-----------------line-------", line)
			for tax in line.tax_id:
				print("----------tax-------", tax)
				print("-----------------------1----------------", line.order_id.partner_id.state_id.id)
				print("-----------------------2----------------", line.order_id.warehouse_id.state_id.id)
				if line.order_id.partner_id.state_id.id == line.order_id.warehouse_id.state_id.id:
					print("-----------------yes---------")
					tax_rate = tax.children_tax_ids[0].amount
					tax_percentage = 2*tax_rate
					tax_amount = round((tax_percentage*line.portal_price/(100+tax_percentage))/2, 2)
					price_unit = line.portal_price - 2*tax_amount
					shipping_tax_cgst = round((tax_percentage*line.shipping_charges/(100+tax_percentage))/2, 2)
					shipping_base = line.shipping_charges-2*shipping_tax_cgst
					grand_subtotal = line.portal_price*line.product_uom_qty+line.shipping_charges
					tax_amount_total = tax_amount*line.product_uom_qty+shipping_tax_cgst
					# tax_amount_total = round((tax_percentage*grand_subtotal/(100+tax_percentage))/2, 2)
					price_subtotal = price_unit*line.product_uom_qty+shipping_base
					line.update({
						'price_unit': price_unit,
						'price_subtotal': price_subtotal,
						'c_price_subtotal': price_subtotal,
						'price_tax': 2*tax_amount_total,
						'sgst_rate': tax.children_tax_ids[0].name,
						'sgst_amount': tax_amount_total,
						'cgst_rate': tax.children_tax_ids[1].name,
						'cgst_amount': tax_amount_total,
						'igst_rate': '',
						'igst_amount': 0.0,
						'shipping_charges_untaxed': shipping_base,
						'shipping_charges_tax': 2*shipping_tax_cgst,
						'tax_sum': tax_percentage,
						'subtotal_with_tax': line.portal_price*line.product_uom_qty,
						'grand_subtotal': grand_subtotal
					})
				else:
					print("-----------------no---------")
					tax_rate = tax.children_tax_ids[0].amount
					tax_percentage = 2*tax_rate
					tax_amount = round((tax_percentage*line.portal_price/(100+tax_percentage)), 2)
					price_unit = line.portal_price-tax_amount
					shipping_tax = round((tax_percentage*line.shipping_charges/(100+tax_percentage)), 2)
					shipping_base = line.shipping_charges-shipping_tax
					grand_subtotal = line.portal_price*line.product_uom_qty+line.shipping_charges
					tax_amount_total = tax_amount*line.product_uom_qty+shipping_tax
					# tax_amount_total = round((tax_percentage*grand_subtotal/(100+tax_percentage)), 2)
					price_subtotal = price_unit*line.product_uom_qty+shipping_base
					print("-----------price_unit----------", price_unit)
					print("-----------price_subtotal----------", price_subtotal)
					print("-----------igst_amount----------", tax_amount_total)
					print("-----------tax_sum----------", tax_percentage)
					print("-----------subtotal_with_tax----------", line.portal_price*line.product_uom_qty)
					print("-----------grand_subtotal----------", grand_subtotal)

					# print("-----------tax_percentage----------", tax_percentage)
					# print("-----------line.grand_subtotal----------", grand_subtotal)
					# print("-----------round((tax_percentage*line.grand_subtotal/(100+tax_percentage)), 2)----------", round((tax_percentage*line.grand_subtotal/(100+tax_percentage)), 2))
					line.update({
						'price_unit': price_unit,
						'price_subtotal': price_subtotal,
						'c_price_subtotal': price_subtotal,
						'price_tax': tax_amount_total,
						'sgst_rate': '',
						'sgst_amount': 0.0,
						'cgst_rate': '',
						'cgst_amount': 0.0,
						'shipping_charges_untaxed': shipping_base,
						'shipping_charges_tax': shipping_tax,
						'igst_rate': 'IGST'+str(tax_percentage)+'%',
						# 'igst_rate': 'IGST'+str(2*float(tax.children_tax_ids[0].amount))+'%',
						'igst_amount': tax_amount_total,
						'tax_sum': tax_percentage,
						'subtotal_with_tax': line.portal_price*line.product_uom_qty,
						'grand_subtotal': grand_subtotal
					})
				print("-----------------end---------")
		return result



class SalePayment(models.Model):
	_name = "sale.payment"


	order_id = fields.Many2one('sale.order', string='SO No.')
	date = fields.Char('Date')
	comission = fields.Char('Commission')
	comission_cgst = fields.Char('Commission CGST')
	comission_igst = fields.Char('Commission IGST')
	comission_sgst = fields.Char('Commission SGST')
	current_reserve_ammount = fields.Char('Current Reserve Amount')
	fba_pick_and_pack = fields.Char('FBA Pick and Pack Fee')
	fba_pick_and_pack_cgst = fields.Char('FBA Pick and Pack Fee CGST')
	fba_pick_and_pack_sgst = fields.Char('FBA Pick and Pack Fee SGST')
	fba_weight_handling_fee = fields.Char('FBA Weight Handling Fee')
	fba_weight_handling_fee_cgst = fields.Char('FBA Weight Handling Fee CGST')
	fba_weight_handling_fee_sgst = fields.Char('FBA Weight Handling Fee SGST')
	fixed_closing_fees = fields.Char('Fixed Closing Fees')
	fixed_closing_fees_cgst = fields.Char('Fixed Closing Fees CGST')
	fixed_closing_fees_sgst = fields.Char('Fixed Closing Fees SGST')
	fixed_closing_fees_igst = fields.Char('Fixed Closing Fees IGST')
	gift_wrap = fields.Char('Gift Wrap')
	gift_wrap_charge_back = fields.Char('Gift Wrap Charge Back')
	gift_wrap_charge_cgst = fields.Char('Gift Wrap Charge CGST')
	gift_wrap_charge_sgst = fields.Char('Gift Wrap Charge SGST')
	gift_wrap_tax = fields.Char('Gift Wrap Tax')
	payment_retraction_item =fields.Char('Payment Retraction Item')
	principal =fields.Char('Principal')
	product_tax =fields.Char('Product Tax')
	product_tax_discount =fields.Char('Product Tax Discount')
	promo_rebates =fields.Char('Promo Rebates')
	refund_commission =fields.Char('Refund Commission')
	refund_commission_igst =fields.Char('Refund Commission IGST')
	removal_complete =fields.Char('Removal Complete')
	removal_complete_cgst =fields.Char('Removal Complete CGST')
	removal_complete_sgst =fields.Char('Removal Complete SGST')
	shipping =fields.Char('Shipping')
	shipping_charge_back =fields.Char('Shipping Chargeback')
	shipping_charge_back_cgst =fields.Char('Shipping ChargeBack CGST')
	shipping_charge_back_sgst =fields.Char('Shipping ChargeBack SGST')
	shipping_discount =fields.Char('Shipping Discount')
	shipping_tax =fields.Char('Shipping Tax')
	shipping_tax_discount =fields.Char('Shipping Tax Discount')
	storage_fee =fields.Char('Storage Fee')
	storage_billing_cgst =fields.Char('Storage Billing CGST')
	storage_billing_sgst =fields.Char('Storage Billing SGST')
	storage_reniew_billing =fields.Char('Storage Renewal Billing')
	storage_reniew_billing_cgst =fields.Char('Storage Renewal Billing CGST')
	storage_reniew_billing_sgst =fields.Char('Storage Renewal Billing SGST')
	tcs_cgst =fields.Char('TCS-CGST')
	tcs_igst =fields.Char('TCS-IGST')
	tcs_sgst =fields.Char('TCS-SGST')
	tds = fields.Char('TDS (Section 194-O)')
	technology_fee =fields.Char('Technology Fee')
	technology_fee_igst =fields.Char('Technology Fee IGST')
