# -*- coding: utf-8 -*-

from odoo import models, fields, osv, api, _
# from odoo.tools.translate import _
# from odoo.tools.float_utils import float_is_zero, float_compare
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
# from odoo.exceptions import Warning, UserError
from datetime import timedelta
# import datetime
# import logging
# import num2words

# _logger = logging.getLogger(__name__)

class AccountMove(models.Model):
	_inherit = "account.move"
	invoice_number = fields.Char(string="Invoice Number", copy=False)
	invoice_number_b2b = fields.Char(string="Invoice Number(B2B)", copy=False)
	sale_number = fields.Char(string="Sale Number", copy=False)
	sale_number_b2b = fields.Char(string="Sale Number(B2B)", copy=False)
	so_id = fields.Many2one('sale.order', string="Sale Order", copy=False)
	order_type = fields.Char(string="Order Type", copy=False)
	order_date = fields.Date(string="Order Date.")
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
	portal_id = fields.Many2one('res.portal', string="Portal", required=True, copy=False)
	warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse", required=True, copy=False)
	sgst = fields.Monetary(string="SGST", store=True, copy=False )
	cgst = fields.Monetary(string="CGST", store=True, copy=False )
	igst = fields.Monetary(string="IGST", store=True, copy=False )
	total_s_c_untaxed = fields.Monetary(string="Total Shipping Untaxed")
	total_s_c_tax = fields.Monetary(string="Total Shipping Tax")
	total_s_c = fields.Monetary(string="Shipping Charge"	)
	order_id = fields.Char(string="Order ID", copy=False)
	is_replacement = fields.Boolean(string="Is Replacement", default=False)
	original_order_id = fields.Char(string="Original Order ID")
	invoice_no = fields.Char(string="Invoice No.", copy=False)
	c_amount_untaxed = fields.Monetary(string="Untaxed Amount", store=True, compute='_amount_all', currency_field='company_currency_id')
	order_category = fields.Selection([('b2b', 'B2B'), ('b2c', 'B2C')], string="Order(B2B/B2C)", required=True, copy=False)
	state_id = fields.Many2one('stock.warehouse', string="State", related='warehouse_id', required=True)

	# Change By Keshav
	def action_post(self):
		res = super(AccountMove, self).action_post()
		# if self.order_category == 'b2c':
		if not self.invoice_number:
			if self.portal_id.name:
				self.invoice_number = '24-25'+'/'+str(self.warehouse_id.inv_code)+'/'+str(self.warehouse_id.next_number_inv_f).zfill(7)
				# self.invoice_number = '22-23'+'/'+str(self.warehouse_id.inv_code)+'/'+str(self.warehouse_id.next_number_inv_f).zfill(7)
				if self.invoice_number:
					wh_inv = self.warehouse_id.write({'next_number_inv_f': self.warehouse_id.next_number_inv_f+1})
			# else:
			# 	self.invoice_number = '23-24'+'/HI/'+str(self.warehouse_id.next_number_inv_o).zfill(7)
			# 	# self.invoice_number = '22-23'+'/HI/'+str(self.warehouse_id.next_number_inv_o).zfill(7)
			# 	if self.invoice_number:
			# 		wh_inv = self.warehouse_id.write({'next_number_inv_o': self.warehouse_id.next_number_inv_o+1})

		# if self.order_category == 'b2c':
		# 	if not self.invoice_number:
		# 		self.invoice_number = '2122'+'C'+'/'+str(self.warehouse_id.code)+'/'+str(self.warehouse_id.next_number).zfill(5)
		# 		if self.invoice_number:
		# 			wh_inv = self.warehouse_id.write({'next_number': self.warehouse_id.next_number+1})
		# if self.order_category == 'b2b':
		# 	if not self.invoice_number_b2b:
		# 		self.invoice_number_b2b = '2122'+'B'+'/'+str(self.warehouse_id.code)+'/'+str(self.warehouse_id.next_number_b2b).zfill(5)
		# 		if self.invoice_number_b2b:
		# 			wh_inv = self.warehouse_id.write({'next_number_b2b': self.warehouse_id.next_number_b2b+1})
		# return False
	@api.onchange('invoice_line_ids.c_price_subtotal')
	@api.depends('invoice_line_ids.c_price_subtotal')
	def _amount_all(self):
		for invoice in self:
			c_amount_untaxed = 0.0
			total_s_c_untaxed = 0.0
			total_s_c_tax = 0.0
			total_s_c = 0.0
			for line in invoice.invoice_line_ids:
				c_amount_untaxed = c_amount_untaxed + line.c_price_subtotal
				total_s_c_untaxed = total_s_c_untaxed + line.shipping_charges_untaxed
				total_s_c_tax = total_s_c_tax + line.shipping_charges_tax
				total_s_c = total_s_c + line.shipping_charges
			invoice.update({
				'c_amount_untaxed': c_amount_untaxed,
				'total_s_c_untaxed': total_s_c_untaxed,
				'total_s_c_tax': total_s_c_tax,
				'total_s_c': total_s_c,
			})
		print("1---------_amount_all----96-self------------", self)
	def _compute_amount(self):
		# print("1--------------self------------", self)
		for move in self:
			# print("2-----------------move---------", move)
			if move.payment_state == 'invoicing_legacy':
				# invoicing_legacy state is set via SQL when setting setting field
				# invoicing_switch_threshold (defined in account_accountant).
				# The only way of going out of this state is through this setting,
				# so we don't recompute it here.
				move.payment_state = move.payment_state
				continue
			total_untaxed = 0.0
			total_untaxed_currency = 0.0
			total_tax = 0.0
			total_tax_currency = 0.0
			total_to_pay = 0.0
			total_residual = 0.0
			total_residual_currency = 0.0
			total = 0.0
			total_currency = 0.0

			# c_amount_untaxed = 0.0
			# total_s_c_untaxed = 0.0
			# total_s_c_tax = 0.0
			# total_s_c = 0.0

			currencies = move._get_lines_onchange_currency().currency_id
			# print("3-----------currencies--move._get_lines_onchange_currency().currency_id---", currencies)
			# print("4------------------move.line_ids--------", move.line_ids)
			for line in move.line_ids:
				# print("5---------------move.is_invoice(include_receipts=True)--------", move.is_invoice(include_receipts=True))
				# c_amount_untaxed = c_amount_untaxed + line.c_price_subtotal
				# total_s_c_untaxed = total_s_c_untaxed + line.shipping_charges_untaxed
				# total_s_c_tax = total_s_c_tax + line.shipping_charges_tax
				# total_s_c = total_s_c + line.shipping_charges
				if move.is_invoice(include_receipts=True):
					# === Invoices ===

					if not line.exclude_from_invoice_tab:
						# Untaxed amount.
						total_untaxed += line.balance
						total_untaxed_currency += line.amount_currency
						total += line.balance
						total_currency += line.amount_currency
					elif line.tax_line_id:
						# Tax amount.
						total_tax += line.balance
						total_tax_currency += line.amount_currency
						total += line.balance
						total_currency += line.amount_currency
					elif line.account_id.user_type_id.type in ('receivable', 'payable'):
						# Residual amount.
						total_to_pay += line.balance
						total_residual += line.amount_residual
						total_residual_currency += line.amount_residual_currency
				else:
					# === Miscellaneous journal entry ===
					if line.debit:
						total += line.balance
						total_currency += line.amount_currency
			if move.move_type == 'entry' or move.is_outbound():
				sign = 1

			else:
				sign = -1
			move.amount_untaxed = sign * (total_untaxed_currency if len(currencies) == 1 else total_untaxed)
			move.amount_tax = sign * (total_tax_currency if len(currencies) == 1 else total_tax)
			move.amount_total = sign * (total_currency if len(currencies) == 1 else total)
			move.amount_residual = -sign * (total_residual_currency if len(currencies) == 1 else total_residual)
			move.amount_untaxed_signed = -total_untaxed
			move.amount_tax_signed = -total_tax
			move.amount_total_signed = abs(total) if move.move_type == 'entry' else -total
			move.amount_residual_signed = total_residual
			currency = len(currencies) == 1 and currencies or move.company_id.currency_id
			# print("-46-------------------------", move.amount_untaxed)
			# print("-48-------------------------", total_untaxed)
			# print("-49-------------------------", total_untaxed_currency)
			# print("-48-------------------------", total_tax)
			# print("-49-------------------------", total_tax_currency)
			# print("-50-------------------------", total_to_pay)
			# print("-51-------------------------", total_residual)
			# print("-52-------------------------", total_residual_currency)
			# print("-53-------------------------", total)
			# print("-54-------------------------", total_currency)
			# print("-55------------------------", currencies)
			# Compute 'payment_state'.
			new_pmt_state = 'not_paid' if move.move_type != 'entry' else False
			if move.is_invoice(include_receipts=True) and move.state == 'posted':
				if currency.is_zero(move.amount_residual):
					reconciled_payments = move._get_reconciled_payments()
					if not reconciled_payments or all(payment.is_matched for payment in reconciled_payments):
						new_pmt_state = 'paid'
					else:
						new_pmt_state = move._get_invoice_in_payment_state()
				elif currency.compare_amounts(total_to_pay, total_residual) != 0:
					new_pmt_state = 'partial'
			if new_pmt_state == 'paid' and move.move_type in ('in_invoice', 'out_invoice', 'entry'):
				reverse_type = move.move_type == 'in_invoice' and 'in_refund' or move.move_type == 'out_invoice' and 'out_refund' or 'entry'
				reverse_moves = self.env['account.move'].search([('reversed_entry_id', '=', move.id), ('state', '=', 'posted'), ('move_type', '=', reverse_type)])

				# We only set 'reversed' state in cas of 1 to 1 full reconciliation with a reverse entry; otherwise, we use the regular 'paid' state
				reverse_moves_full_recs = reverse_moves.mapped('line_ids.full_reconcile_id')
				if reverse_moves_full_recs.mapped('reconciled_line_ids.move_id').filtered(lambda x: x not in (reverse_moves + reverse_moves_full_recs.mapped('exchange_move_id'))) == move:
					new_pmt_state = 'reversed'
			move.payment_state = new_pmt_state
			move.amount_total = round(move.amount_total+move.total_s_c)

			# move.c_amount_untaxed = c_amount_untaxed
			# move.total_s_c_untaxed = total_s_c_untaxed
			# move.total_s_c_tax = total_s_c_tax
			# move.total_s_c = total_s_c
			# print("-56------move.amount_total-------------------", move.amount_total)
			# print("-56-------------------------", total_untaxed)
			# print("-57-------------------------", total_untaxed_currency)
			# print("-58-------------------------", total_tax)
			# print("-59-------------------------", total_tax_currency)
			# print("-60-------------------------", total_to_pay)
			# print("-61-------------------------", total_residual)
			# print("-62-------------------------", total_residual_currency)
			# print("-63-------------------------", total)
			# print("-64-------------------------", total_currency)
			# print("-65------------------------", currencies)
		#--------------------custom----------------------------------------------------------
		# for invoice in self:
		# 	c_amount_untaxed = 0.0
		# 	total_s_c_untaxed = 0.0
		# 	total_s_c_tax = 0.0
		# 	total_s_c = 0.0
		# 	for line in invoice.invoice_line_ids:
		# 		c_amount_untaxed = c_amount_untaxed + line.c_price_subtotal
		# 		total_s_c_untaxed = total_s_c_untaxed + line.shipping_charges_untaxed
		# 		total_s_c_tax = total_s_c_tax + line.shipping_charges_tax
		# 		total_s_c = total_s_c + line.shipping_charges
		# 	invoice.update({
		# 		'c_amount_untaxed': c_amount_untaxed,
		# 		'total_s_c_untaxed': total_s_c_untaxed,
		# 		'total_s_c_tax': total_s_c_tax,
		# 		'total_s_c': total_s_c,
		# 	})
		# print("1---------_amount_all----96-self------------", self)
	def _inverse_amount_total(self):
		for move in self:
			if len(move.line_ids) != 2 or move.is_invoice(include_receipts=True):
				continue
			to_write = []
			amount_currency = abs(move.amount_total)
			balance = move.currency_id._convert(amount_currency, move.company_currency_id, move.company_id, move.date)
			for line in move.line_ids:
				if not line.currency_id.is_zero(balance - abs(line.balance)):
					to_write.append((1, line.id, {
						'debit': line.balance > 0.0 and balance or 0.0,
						'credit': line.balance < 0.0 and balance or 0.0,
						'amount_currency': line.balance > 0.0 and amount_currency or -amount_currency,
					}))
			move.write({'line_ids': to_write})

class AccountMoveLine(models.Model):
	_inherit = "account.move.line"
	product_hsn = fields.Char(string="HSN Code.")
	# product_hsn = fields.Char(related='product_id.product_tmpl_id.l10n_in_hsn_code', string="HSN Code.")
	sku_name = fields.Char(string="SKU Id")
	portal_price = fields.Monetary(string="Portal Price", store=True)
	shipping_charges = fields.Monetary(string="Shipping Charge")
	shipping_charges_untaxed = fields.Monetary(string="Shipping Charge Untaxed", store=True)
	shipping_charges_tax = fields.Monetary(string="Shipping Charge Tax", store=True)
	sgst_rate = fields.Char(string="SGST@", store=True)
	sgst_amount = fields.Monetary(string="SGST Amt", store=True)
	cgst_rate = fields.Char(string="CGST@", store=True)
	cgst_amount = fields.Monetary(string="CGST Amt", store=True)
	igst_rate = fields.Char(string="IGST@", store=True)
	igst_amount = fields.Monetary(string="IGST Amt", store=True)
	tax_sum = fields.Monetary(string="Tax Sum", store=True)
	price_tax = fields.Float(string="Price Tax", store=True)
	subtotal_with_tax = fields.Monetary(string="Subtotal With Tax", store=True)
	grand_subtotal = fields.Monetary(string="Grand Subtotal", store=True)
	c_price_subtotal = fields.Monetary(string="Subtotal", store=True, compute='_compute_amount', currency_field='company_currency_id')
	gift_wrap_price = fields.Monetary(string="Gift Wrap price")
	item_promo_discount = fields.Monetary(string="Item Promo Discount")


	# @api.model_create_multi
	# def create(self, vals_list):
	# 	result = super(AccountMoveLine, self).create(vals_list)
	# 	print("------ac--print @@@------------")
	# 	return result
	# 	self._compute_amount()

	@api.onchange('product_id', 'price_unit', 'product_uom', 'quantity', 'tax_ids', 'portal_price', 'shipping_charges')
	# @api.depends('product_id', 'price_unit', 'quantity', 'tax_ids', 'portal_price', 'shipping_charges')
	def _compute_amount(self):
		# result = super(SaleOrderLine, self)._compute_amount()
		print("---------------ac--self-------", self)
		for line in self:
			print("-----------------line-------", line)
			for tax in line.tax_ids:
				print("----------tax-------", tax)
				print("-----------------------1----------------", line.move_id.partner_id.state_id.id)
				print("-----------------------2----------------", line.move_id.warehouse_id.state_id.id)
				if line.move_id.partner_id.state_id.id == line.move_id.warehouse_id.state_id.id:
					print("-----------------yes---------")
					tax_rate = tax.children_tax_ids[0].amount
					tax_percentage = 2*tax_rate
					tax_amount = round((tax_percentage*line.portal_price/(100+tax_percentage))/2, 2)
					price_unit = line.portal_price - 2*tax_amount
					shipping_tax_cgst = round((tax_percentage*line.shipping_charges/(100+tax_percentage))/2, 2)
					shipping_base = line.shipping_charges-2*shipping_tax_cgst
					grand_subtotal = line.portal_price*line.quantity+line.shipping_charges
					tax_amount_total = tax_amount*line.quantity+shipping_tax_cgst
					price_subtotal = price_unit*line.quantity+shipping_base
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
						'subtotal_with_tax': line.portal_price*line.quantity,
						'grand_subtotal': grand_subtotal
					})
					# print("----------------------------line.portal_price------------", line.portal_price)
					# print("----------------------------line.quantity------------", line.quantity)
					# print("----------------------------dfg------------", self.subtotal_with_tax)
					# line.subtotal_with_tax = line.portal_price*line.quantity,
				else:
					print("-----------------no---------")
					tax_rate = tax.children_tax_ids[0].amount
					tax_percentage = 2*tax_rate
					tax_amount = round((tax_percentage*line.portal_price/(100+tax_percentage)), 2)
					price_unit = line.portal_price-tax_amount
					shipping_tax = round((tax_percentage*line.shipping_charges/(100+tax_percentage)), 2)
					shipping_base = line.shipping_charges-shipping_tax
					grand_subtotal = line.portal_price*line.quantity+line.shipping_charges
					tax_amount_total = (tax_amount+shipping_tax)*line.quantity
					price_subtotal = price_unit*line.quantity+shipping_base
					print("-----------price_unit----------", price_unit)
					print("-----------price_subtotal----------", price_subtotal)
					print("-----------igst_amount----------", tax_amount_total)
					print("-----------tax_sum----------", tax_percentage)
					print("-----------subtotal_with_tax----------", line.portal_price*line.quantity)
					print("-----------grand_subtotal----------", grand_subtotal)

					# print("-----------tax_percentage----------", tax_percentage)
					# print("-----------line.grand_subtotal----------", grand_subtotal)
					# print("-----------round((tax_percentage*line.grand_subtotal/(100+tax_percentage)), 2)----------", round((tax_percentage*line.grand_subtotal/(100+tax_percentage)), 2))
					line.write({
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
						'subtotal_with_tax': line.portal_price*line.quantity,
						'grand_subtotal': grand_subtotal
					})
					# print("----------------------------dfg------------", self.subtotal_with_tax)
					# line.subtotal_with_tax = line.portal_price*line.quantity,
				print("-----------------end---------")
		print("-----------------yes do it---------")
		# return result
