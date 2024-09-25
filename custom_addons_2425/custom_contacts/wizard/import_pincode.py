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
	_name = 'import.pincode'
	_description = 'Import pincode'

	csv_file = fields.Binary(string='CSV File', required=True, help='File should be separated by comma (,) and quoted using Quote character (") ')
	country_id = fields.Many2one('res.country', string="Country", required=True)
	state_id = fields.Many2one('res.country.state', string="State", domain="[('country_id', '=', country_id)]")

	def import_pincode(self):
		pincode_pool = self.env['res.partner']
		state_pool = self.env['res.country.state']
		country_pool = self.env['res.country']
		f = base64.b64decode(self.csv_file)
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
		for row in reader:
			print("------------------------------p1--------------------------")
			pincode = row[headers['Pincode']].strip()
			state = row[headers['State']].strip()
			# if not self.env['pincode.state'].search([('name', '=', pincode)]):
			if not self.env['pincode.state'].search([('name', '=', pincode)]):
				state_id = self.env['res.country.state'].search([('name', '=', state)])
				pincode_vals = {
						'name': pincode,
						'district': row[headers['District']].strip(),
						'country_id': self.country_id.id,
						'state_id': state_id.id
				}
				# print("----------pincode_vals-------", pincode_vals)
				p_s = self.env['pincode.state'].create(pincode_vals)
				print("--------p_s--------------", p_s)
			count = count+1
			print("------------------------count---------------", count)
