# -*- coding: utf-8 -*-
import xlwt
import base64
import calendar
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
from odoo.exceptions import Warning, UserError
import logging

_logger = logging.getLogger(__name__)


class EXportProducts(models.TransientModel):
	_name = 'export.products'
	_description = 'Export products'

	file_name = fields.Char(string='Name', size=256)
	file_xls = fields.Binary(string='Report', readonly=True)
	flag = fields.Boolean(string="Flag")

	def export_products_xls(self):
		print("============export_products_xls==============")
		workbook = xlwt.Workbook()
		ws = workbook.add_sheet('Sheet1')
		s_h = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center")
		print("---------------------------------writting into sheet--------------------")
		ws.write(0, 0, 'Product Name', s_h)
		ws.write(0, 1, 'Internal Reference', s_h)
		ws.write(0, 2, 'Brand', s_h)
		ws.write(0, 3, 'Product Preparation', s_h)
		ws.write(0, 4, 'Taxes(%)', s_h)
		ws.write(0, 5, 'HSN', s_h)
		ws.write(0, 6, 'SKU ID', s_h)
		product_ids = self.env['product.product'].search([])
		if product_ids:
			row = 1
			for pro_id in product_ids:
				ws.write(row, 0, pro_id.name)
				ws.write(row, 1, pro_id.default_code)
				ws.write(row, 2, pro_id.brand_id.name)
				ws.write(row, 3, pro_id.p_prepartion_id)
				ws.write(row, 4, pro_id.taxes_id.name)
				ws.write(row, 5, pro_id.l10n_in_hsn_code)
				if pro_id.sku_line_id:
					for sku_l in pro_id.sku_line_id:
						ws.write(row, 6, sku_l.name)
						row+=1
				else:
					row+=1    
		else:
			raise Warning("Currently, There is No Product!")
		filename = 'Product_List'+ '.xls'
		workbook.save(filename)
		file = open(filename, "rb")
		file_data = file.read()
		out = base64.encodestring(file_data)
		self.write({'file_name': filename, 'file_xls':out, 'flag': True})
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'export.products',
			'view_mode': 'form',
			'view_type': 'form',
			'res_id': self.id,
			'target': 'new',
		}