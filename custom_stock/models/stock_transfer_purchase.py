# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.exceptions import Warning, UserError

class StockTranferPurchase(models.Model):
	_name = 'stock.transfer.purchase'
	_description = 'Stock Tranfer Purchase'
	# _order = 'sequence'
	# _order = "name desc"
	_sql_constraints = [
	('ord_id_uniq', 'unique(ord_id)', "A Order Id can only be assigned to one Tranfer !")
	]
	name = fields.Char(string="Number", index=True, copy=False, readonly=True, default='New')
	sale_invoice = fields.Char(string="Sale Invoice", index=True, copy=False, readonly=True)
	ship_from_fc = fields.Many2one('stock.warehouse', string="Ship From Fc", required=True)
	gstin = fields.Char(related="ship_from_fc.gstin", string="GSTIN(Supplier)", store=True)
	state_id = fields.Many2one(related="ship_from_fc.state_id", string="State(Supplier)", store=True)
	ship_to_fc = fields.Many2one('stock.warehouse', string="Ship To Fc", required=True)
	debit_note = fields.Boolean(string="Debit Note", default=False)
	receipt = fields.Boolean(string="Receipt", default=False, compute='comp_receipt', store=True)
	trn_type = fields.Selection([('fcr', 'FC_REMOVAL'), ('fcrc', 'FC_REMOVAL-Cancel'), ('fct', 'FC_TRANSFER')], string="Transaction Type")
	ord_id = fields.Char(string="Order Id")
	stock_transfer = fields.Many2one('stock.transfer', string="Stock Tranfer ID Odoo(Records)")
	transfer_id_odoo = fields.Many2one('stock.picking', string="Stock Picking ID Odoo")
	month_of_stock_trns = fields.Selection([
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
        ], string="Month of Stock Tranfer", default=False)
	invoice_date = fields.Datetime(string="Invoice Date")
	invoice_no = fields.Char(string="Invoice Number")
	stock_transfer_line = fields.One2many('stock.transfer.purchase.line', 'stock_transfer_purchase_id', string='Stock Tranfer Purchse Lines', copy=True, auto_join=True)
	company_id = fields.Many2one(related='ship_from_fc.company_id', string='Company', store=True, readonly=True, index=True)
	currency_id = fields.Many2one(related='company_id.currency_id', string="Currency ID")
	state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, default='draft')
	total_taxable_value = fields.Monetary(string="Total Taxable Value", store=True, readonly=True, compute='_amount_all')
	total_igst_amount = fields.Monetary(string="Total Igst Amount", store=True, readonly=True, compute='_amount_all')
	other_charges = fields.Monetary(string="Other Charges")
	total_invoice_vales = fields.Monetary(string="Total Bill Value", store=True, readonly=True, compute='_amount_all')

	# sgst_rate = fields.Char(string="Sgst Rate")
	# sgst_amount = fields.Monetary(string="Sgst Amount")
	# utgst_rate = fields.Char(string="Utgst Rate")
	# utgst_amount = fields.Monetary(string="Utgst Amount")
	# cgst_rate = fields.Char(string="Cgst Rate")
	# cgst_amount = fields.Monetary(string="Cgst Amount")
	# comp_c_r = fields.Char(string="Compensatory Cess Rate")
	# comp_c_a = fields.Monetary(string="Compensatory Cess Amount")
	# gstin_of_receiver = fields.Char(string="Gstin Of Receiver")
	# trn_type = fields.Selection([('fcr', 'FC_REMOVAL'), ('fcrc', 'FC_REMOVAL-Cancel'), ('fct', 'FC_TRANSFER')], string="Transaction Type")
	# trans_id = fields.Char(string="Transaction Id")
	# ship_from_city = fields.Char(string="Ship From City")
	# ship_from_state = fields.Char(string="Ship From State")
	# ship_from_country = fields.Char(string="Ship From Country")
	# ship_f_p_c = fields.Char(string="Ship From Postal Code")
	# ship_to_city = fields.Char(string="Ship To City")
	# ship_to_state = fields.Char(string="Ship To State")
	# ship_to_country = fields.Char(string="Ship To Country")
	# ship_to_p_c = fields.Char(string="Ship To Postal Code")
	# gstin_of_supplier = fields.Char(string="Gstin Of Supplier")
	# irn_no = fields.Char(string="Irn Number")
	# irn_f_s = fields.Char(string="Irn Filing Status")
	# irn_date = fields.Char(string="Irn Date")
	# irn_e_c = fields.Char(string="Irn Error Code")
	@api.depends('stock_transfer_line.invoice_vales')
	def _amount_all(self):
		for order in self:
			total_taxable_value = total_igst_amount = 0.0
			for line in order.stock_transfer_line:
				total_taxable_value += line.taxable_value
				total_igst_amount += line.igst_amount
			order.update({
				'total_taxable_value': total_taxable_value,
				'total_igst_amount': total_igst_amount,
				'total_invoice_vales': total_taxable_value + total_igst_amount
			})

	# Change By Keshav
	@api.model
	def create(self, vals):
		# print("-----------------------create------1--------------")
		res = super(StockTranferPurchase, self).create(vals)
		if res.ship_to_fc:
			new_seq = '23-24'+'/'+res.ship_to_fc.code+'/'+str(res.ship_to_fc.next_number_s_t_p).zfill(5)
			# new_seq = '21-22'+'/'+res.ship_to_fc.code+'/'+str(res.ship_to_fc.next_number_s_t_p).zfill(5)
			true_false = res.write({'name': new_seq})
			if true_false:
				res.ship_to_fc.write({'next_number_s_t_p': res.ship_to_fc.next_number_s_t_p+1})
		return res
	@api.depends('ship_to_fc', 'ship_from_fc')
	@api.onchange('ship_to_fc', 'ship_from_fc')
	def comp_receipt(self):
		# for p_l in self.env['stock.transfer.purchase.line'].search([('stock_transfer_purchase_id', '=', self.id)]):
		# 	print("-----------------234------", p_l._onchange_product())
		for line in self:
			if line.ship_to_fc.state_id and line.ship_from_fc.state_id:
				if line.ship_to_fc.state_id.name == line.ship_from_fc.state_id.name:
					line.update({'receipt': True})

class StockTranferPurchaseLine(models.Model):
	_name = 'stock.transfer.purchase.line'
	_description = 'Stock Tranfer Purchase Line'
	stock_transfer_purchase_id = fields.Many2one('stock.transfer.purchase', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
	product_product_id = fields.Many2one("product.product", string="Product")
	name = fields.Char(string='Product Name', store=True)
	default_code = fields.Char(related="product_product_id.default_code", string="Product Id", store=True)
	sku = fields.Char(string="Sku")
	asin = fields.Char(string="Asin")
	l10n_in_hsn_code = fields.Char(string="Hsn Code", store=True, readonly=True)
	unit_price = fields.Monetary(string="Unit Price")
	quntity = fields.Float(string="Quantity")
	taxes_id = fields.Many2many('account.tax', string="Taxes")
	currency_id = fields.Many2one(related='stock_transfer_purchase_id.currency_id', string="Currency ID")
	taxable_value = fields.Monetary(string="Taxable Value")
	igst_rate = fields.Float(string="Igst Rate")
	igst_amount = fields.Monetary(string="Igst Amount")
	other_charges = fields.Monetary(string="Other Charges")
	invoice_vales = fields.Monetary(string="Bill Value", store=True)
	purchase_ladgers = fields.Char(string="Purchase Ledgers")
	trans_id = fields.Char(string="Transaction Id")
	invoice_no = fields.Char(string="Amazon Invoice Number")
	stock_transfer = fields.Many2one('stock.transfer', string="Stock Tranfer ID Odoo(Records)")
	@api.model
	def create(self, vals):
		# print("-----------------------create------2--------------")
		res = super(StockTranferPurchaseLine, self).create(vals)
		res._onchange_product()
		res.compute_amount()
		return res
	@api.depends('product_product_id')
	@api.onchange('product_product_id')
	def _onchange_product(self):
		if not self.product_product_id:
			return
		self.l10n_in_hsn_code = self.product_product_id.l10n_in_hsn_code
		self.name = self.product_product_id.product_tmpl_id.name
		self.taxes_id = self.product_product_id.taxes_id
		self.compute_amount()
	@api.onchange('quntity', 'invoice_vales')
	# @api.onchange('quntity', 'invoice_vales', 'stock_transfer_purchase_id.ship_to_fc', 'stock_transfer_purchase_id.ship_from_fc')
	def compute_amount(self):
		# print("--------------------compute_amount----------")
		if not self.product_product_id:
			return
		# print("---------------self----", self)
		# print("---------------self111----", self.quntity)
		# print("---------------self1222----", self.name)
		# print("---------------self4444----", self.product_product_id)
		for line in self:
			# print("------------ line.product_product_id.taxes_id------------",  line.product_product_id.taxes_id)
			vals={
				'invoice_vales': line.invoice_vales,
				'quntity': line.quntity,
			}
			# print("--------------line.invoice_vales----------", line.invoice_vales)
			# print("--------------line.quntity----------", line.quntity)
			for tax in line.product_product_id.taxes_id:
				s_l = tax.amount
				# print("--------s_l-------", s_l)
				quntity = line.quntity
				invoice_vales = line.invoice_vales
				tax_rate =0.0
				taxable_amount =0.0
				taxable_value = 0.0
				if line.stock_transfer_purchase_id.ship_to_fc.state_id.name != line.stock_transfer_purchase_id.ship_from_fc.state_id.name:
					vals['purchase_ladgers'] = 'Br. Purchase-IGST-'+str(int(s_l))+'%'
					# vals['purchase_ladgers'] = 'Br. Purchase-IGST-'+str(int(s_l))+'%' if s_l else ''
					vals['igst_rate']=tax_rate = 2*tax.children_tax_ids[0].amount
					vals['taxable_value'] =taxable_value= round(invoice_vales*100/(100+tax_rate), 2)
					vals['igst_amount'] = taxable_amount = invoice_vales-taxable_value
					vals['unit_price'] = unit_price = taxable_value/quntity if quntity else 0.0
					# print("-------------tax_rate-------", tax_rate)
					# print("-------------tax_rate-------", taxable_value)
					# print("-------------tax_rate-------", taxable_amount)
				if line.stock_transfer_purchase_id.ship_to_fc.state_id.name == line.stock_transfer_purchase_id.ship_from_fc.state_id.name:
					vals['purchase_ladgers'] = 'Br. Purchase-IGST-'+str(0)+'%'
					# vals['purchase_ladgers'] = 'Br. Purchase-IGST-'+str(0)+'%' if s_l else ''
					vals['taxable_value'] = invoice_vales
					vals['unit_price'] = unit_price = invoice_vales/quntity if quntity else 0.0
					vals['igst_rate']= 0.0
					vals['igst_amount'] = 0.0
					# print("--------------------taxable_value----------", taxable_value)
				if line.quntity > 0:
					# print("--------------------line.quntity----------", line.quntity)
					# print("---------------------vals------------", vals)
					line.update(vals)