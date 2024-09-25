# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.exceptions import Warning, UserError

class StockTranfer(models.Model):
	_name = 'stock.transfer'
	_description = 'Stock Tranfer'
	# _order = 'sequence'
	# _order = "name desc"
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
	gstin_of_receiver = fields.Char(string="Gstin Of Receiver")
	trn_type = fields.Selection([('fcr', 'FC_REMOVAL'), ('fcrc', 'FC_REMOVAL-Cancel'), ('fct', 'FC_TRANSFER')], string="Transaction Type")
	trans_id = fields.Char(string="Transaction Id")
	ord_id = fields.Char(string="Order Id")
	ship_from_fc = fields.Char(string="Ship From Fc")
	ship_from_city = fields.Char(string="Ship From City")
	ship_from_state = fields.Char(string="Ship From State")
	ship_from_country = fields.Char(string="Ship From Country")
	ship_f_p_c = fields.Char(string="Ship From Postal Code")
	ship_to_fc = fields.Char(string="Ship To Fc")
	ship_to_city = fields.Char(string="Ship To City")
	ship_to_state = fields.Char(string="Ship To State")
	ship_to_country = fields.Char(string="Ship To Country")
	ship_to_p_c = fields.Char(string="Ship To Postal Code")
	invoice_no = fields.Char(string="Invoice Number")
	invoice_date = fields.Datetime(string="Invoice Date")
	currency_id = fields.Many2one("res.currency", string="Currency ID")
	invoice_vales = fields.Monetary(string="Invoice Value", store=True)
	asin = fields.Char(string="Asin")
	sku = fields.Char(string="Sku")
	quntity = fields.Float(string="Quantity")
	hsn_code = fields.Char(string="Hsn Code")
	taxable_value = fields.Monetary(string="Taxable Value")
	igst_rate = fields.Char(string="Igst Rate")
	igst_amount = fields.Monetary(string="Igst Amount")
	sgst_rate = fields.Char(string="Sgst Rate")
	sgst_amount = fields.Monetary(string="Sgst Amount")
	utgst_rate = fields.Char(string="Utgst Rate")
	utgst_amount = fields.Monetary(string="Utgst Amount")
	cgst_rate = fields.Char(string="Cgst Rate")
	cgst_amount = fields.Monetary(string="Cgst Amount")
	comp_c_r = fields.Char(string="Compensatory Cess Rate")
	comp_c_a = fields.Monetary(string="Compensatory Cess Amount")
	gstin_of_supplier = fields.Char(string="Gstin Of Supplier")
	irn_no = fields.Char(string="Irn Number")
	irn_f_s = fields.Char(string="Irn Filing Status")
	irn_date = fields.Char(string="Irn Date")
	irn_e_c = fields.Char(string="Irn Error Code")
	# def create(self):
	# 	res = super(StockTranfer, self).create()