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


class ImportWarehouse(models.TransientModel):
	_name = 'import.warehouse'
	_description = 'Import Warehouse'

	warehouse_file = fields.Binary(string='CSV File', help='File should be separated by comma (,) and quoted using Quote character (") ')

	def import_warehouse(self):
		partner_pool = self.env['res.partner']
		warehouse_pool = self.env['stock.warehouse']
		f = base64.b64decode(self.warehouse_file)
		data_file = io.StringIO(f.decode("utf-8"))
		reader = csv.reader(data_file, delimiter=',')
		headers = {}
		for row in reader:
			col_count = 0
			for col in row:
				headers[col] = col_count
				col_count = col_count + 1
			break;
		count = 2
		for row in reader:
			state = row[headers['State']].strip()
			state_id = self.env['res.country.state'].search([('country_id', '=', 104), ('name', '=', state)]).id
			if state_id:
				pass
			else:
				raise UserError(_("State "+state+' in line '+str(count)+' is not found'))
		data_file.seek(0)
		headers = {}
		for row in reader:
			col_count = 0
			for col in row:
				headers[col] = col_count
				col_count = col_count + 1
			break;
		product = ''
		attri_name = ''
		p_t_line_id = ''
		count =2
		for row in reader:
			print("------------------------------p1--------------------------")
			state_id = self.env['res.country.state'].search([('country_id', '=', 104), ('name', '=', row[headers['State']].strip())]).id
			partner_vals = {
					'name': row[headers['Warehouse Name']].strip(),
					'street': row[headers['Complete Adress']].strip(),
					# 'street2': row[headers['Road']].strip(),
					'city': row[headers['City']].strip(),
					'zip': row[headers['Pincode']].strip(),
					'country_id': 104,
					'state_id': state_id,
					'vat': row[headers['GSTIN No.']].strip(),
			}
			print("----------partner_vals-------", partner_vals)
			p_c = partner_pool.create(partner_vals)
			print("--------p_c--------------", p_c)
			warehouse_vals = {
					'name': row[headers['Warehouse Name']].strip(),
					'code': row[headers['Warehouse Code']].strip(),
					'inv_code': row[headers['Flipkart Codes']].strip(),
					'b2b_code': row[headers['B2B Code']].strip(),
					'ownership': row[headers['Ownership']].strip(),
					'partner_id': p_c.id
			}
			w_c = warehouse_pool.create(warehouse_vals)
			print("--------w_c--------------", w_c)
			count = count+1
			print("------------------------count---------------", count)

	# def import_warehouse_state(self):
	# 	partner_pool = self.env['res.partner']
	# 	warehouse_pool = self.env['stock.warehouse']
	# 	f = base64.b64decode(self.warehouse_file)
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
	# 		print("------------------------------p1--------------------------", row[headers['State']].strip())
	# 		state_id = self.env['res.country.state'].search([('name', '=', row[headers['State']].strip()), ('country_id', '=', 104)])[0].id
	# 		w_id = self.env['stock.warehouse'].search([('code', '=', row[headers['Short Name']].strip())])
	# 		updated_w = w_id.update({'state_id': state_id})
	# 		updated_partner = w_id.partner_id.update({'state_id': state_id})
	# 		print("------------------------------updated_w--------------------------", updated_w)
	# 		print("------------------------------updated_partner--------------------------", updated_partner)