# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
# from openerp.tools.translate import _
# from openerp import tools, api
# from openerp import SUPERUSER_ID
import xmlrpc.client

url = "http://192.168.1.4:8081"
db = "healthgenie_new_db_3april2024"
#db = "sinew_fy2122"
username = "admin"
password = "admin123"

# common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# uid = common.authenticate(db, username, password, {})
# models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
# from datetime import datetime, timedelta
import csv
# import tempfile
# import StringIO
from datetime import datetime
import io
import base64
import datetime as dt
from odoo.exceptions import Warning, UserError
import logging
_logger = logging.getLogger(__name__)

class ImportReturnOrder(models.TransientModel):
	_name = 'import.return.order'
	_description = 'Import Return Order'
	return_order_file = fields.Binary(string='CSV File', help='File should be separated by comma (,) and quoted using Quote character (") ')
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
        ], string="Month of Return", default=False)
	def action_confirm(self):
		print("-----Running Action Confirm-----", self)
		rto_ids = self.env['return.order'].search([('state', '=', 'draft')], order='id asc')
		print("-------------------------rto_ids--------", rto_ids)
		for rto in rto_ids:
			print("-------------------------rto--------", rto)
			rto.action_confirm()
			# rto._action_confirm_return_order()
			print("-------------------------rto--------", rto)
	# def action_confirm_return_2023_05_30(self):
	# 	print('-------------my function was called----------', self)
	# 	rto_ids = self.env['return.order'].search([('state', '=', 'draft')], order='id asc')
	# 	for i in rto_ids:
	# 		print('-------------\n\n------', i._fields)
	# 		i.state = 'done'
	# 		# i.action_confirm()
	# 		print('----------\n\n----------', i.state)

	# def o_order_o_db(self, order_id, product_id, count):
	# 	print('--------o-db', order_id, product_id, count)
	# 	# url = "http://localhost:8069"
	# 	# db = "sinew_fy2122"
	# 	# username = "admin"
	# 	# password = "admin@0104"
	# 	common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
	# 	uid = common.authenticate(db, username, password, {})
	# 	models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
	# 	# print('------common----', common)
	# 	# print('------UID----', uid)
	# 	# print('------models----', models)
	# 	inv_ids = models.execute_kw(db, uid, password, 'account.move', 'search_read', [[['order_id', '=', order_id]]], {'fields': ['is_replacement', 'original_order_id', 'amount_total']})
	# 	print('====================',inv_ids)
	# 	inv_line_id = ''
	# 	# print("----------------------------inv_ids--------------", inv_ids)
	# 	if not inv_ids:
	# 		raise UserError(_("Order ID "+order_id+' in line '+str(count)+' is not found in Previous Database'))
	# 	if not inv_ids[0]:
	# 		raise UserError(_("Order ID "+order_id+' in line '+str(count)+' is not found in Previous Database'))
	# 	if inv_ids[0]:
	# 		# print("----------------------------inv_ids['is_replacement']--------------", inv_ids[0]['is_replacement'])
	# 		# print("----------------------------inv_ids['is_replacement']-----t---------", type(inv_ids[0]['is_replacement']))
	# 		if inv_ids[0]['is_replacement'] == True:
	# 			return  self.o_order_o_db(inv_ids[0]['original_order_id'], product_id, count)
	# 		elif inv_ids[0]['amount_total'] > 0:
	# 			inv_line_ids = models.execute_kw(db, uid, password, 'account.move.line', 'search', [[['move_id', '=', inv_ids[0]['id']], ['sku_name', '=', product_id]]])
	# 			print("s:::::::::::::::::::::",inv_line_ids)
	# 			if not inv_line_ids:
	# 				raise UserError(_("Invoice product is not found in privious Database as "+product_id+' in line '+str(count)))
	# 			return 0
	# 		else:
	# 			raise UserError(_("Invoice value must be grater than 0 for "+order_id+' in line '+str(count)))

	# 	# print("---------------partner------", inv_ids)
	# 	# print("---------------partner---t---", type(inv_ids))
	
	def original_order(self, order_id, product_id, count):
		print("-----------------order_idgggggg--------------",order_id,product_id)

		# o_i_id = ''
		inv_id = self.env['account.move'].search([('order_id', '=', order_id),('state', '=', 'posted')])
		print("inv_id::::::::::::::::",inv_id)
		print("-----------------order_id--------------",inv_id.order_id)
		print("-----------------order_id11--------------",order_id)
		print("-----------------state--------------",inv_id.state)


		# o_i_id = inv_id
		inv_id_o_db = ''
		if not inv_id:
			# return 0
			return (order_id, product_id, count)
			# call db previous year
		# 	raise UserError(_("Order ID "+order_id+' in line '+str(count)+' is not already exist'))
		else:
			if inv_id.is_replacement == True and inv_id.original_order_id:
				return self.original_order(inv_id.original_order_id, product_id, count)
			elif inv_id.amount_total > 0.0:
				invoice_line_id = self.env['account.move.line'].search([('move_id', '=', inv_id.id), ('sku_name', '=', product_id)])
				print("invoice_line_id::::::::::::::::::::::::::::::",invoice_line_id)
				if not invoice_line_id:
					# raise UserError(_("Invoice product is not found as "+product_id+' in line '+str(count)))
					raise UserError(_("The product of FSN in line "+str(count)+' is not in order id '+order_id))
				return inv_id.id
			else:
				raise UserError(_("Invoice value must be grater than 0 for "+order_id+' in line '+str(count)))


				# inv_rpl_id = self.env['account.move'].search([('order_id', '=', inv_id[0].original_order_id)])
				# if not inv_rpl_id:
				# 	raise UserError(_("Order ID "+o_i+' in line '+str(count)+' as replacement order id of original order id of '+inv_id[0].original_order_id+'is not already exist'))
				# if inv_rpl_id and inv_rpl_id[0].is_replacement == True:
				# 	inv_rpl2_id = self.env['account.move'].search([('order_id', '=', inv_rpl_id[0].original_order_id)])
				# 	if not inv_rpl2_id:
				# 		raise UserError(_("Order ID "+o_i+' in line '+str(count)+' as replacement order id of original order id of '+inv_rpl_id[0].original_order_id+'is not already exist'))
		# if o_i_id ==  0:
		# 	return 0
		# if inv_id.amount_total > 0.0:
		# 	return inv_id.id
		# else:
		# 	# return 0
		# 	raise UserError(_("Order ID "+order_id+' in line '+str(count)+' has not price values'))

	def import_rto(self):
		print('---------RTO------')
		f = base64.b64decode(self.return_order_file)
		data_file = io.StringIO(f.decode("utf-8"))
		reader = csv.reader(data_file, delimiter=',')
		headers = {}
		for row in reader:
			col_count = 0
			for col in row:
				headers[col] = col_count
				col_count = col_count + 1
			break;
		# print("------------headers------", headers)
		#----------------------------------------------------one-time-check----------------------------------------------------
		count =1
		p_r_d = ''
		for row in reader:
			count+=1
			r_d = datetime.strptime(row[headers['Return Date']].strip(), "%d/%m/%Y").date()
			if not p_r_d:
				p_r_d = r_d
				continue;
			if p_r_d and p_r_d > r_d:
				raise Warning(_("Return Date must be in increasing order."))
			else:
				p_r_d = r_d
			# if count >= 4:
			#     break
			# print("------------break------")
		#----------------------------------------------------check-order----------------------------------------------------
		data_file.seek(0)
		headers = {}
		for row in reader:
			col_count = 0
			for col in row:
				headers[col] = col_count
				col_count = col_count + 1
			break;
		count =2
		print("------------------count--------------", count)
		print("------------headers------", headers)
		warehouse_ids = self.env['stock.warehouse'].search([])
		warehouse_code = [k.code for k in warehouse_ids]
		for row in reader:
			rto_no = row[headers['RTO No']].strip()
			rto_no_id = self.env['return.order'].search([('return_o_no', '=', rto_no)])
			if rto_no_id:
				raise UserError(_("RTO No "+rto_no+' in line '+str(count)+' is already exist in RTO Order'))
		

			fsn = row[headers['FSN']].strip()
			if not fsn:
				raise UserError(_("FSN "+fsn+' in line '+str(count)+' is mandatory'))
			fsn_id = self.env['sku.mapping'].search([('id_number', '=', fsn)])
			print('*******************************************************', fsn_id)
			if not fsn_id:
				raise UserError(_("FSN "+fsn+' in line '+str(count)+' is not found. update in SKU Mapping'))
			o_i = row[headers['Order ID']].strip()
			print('o_i::::::::::::::::::::::::::', o_i)
			if not o_i:
				raise UserError(_("Order ID "+o_i+' in line '+str(count)+' is mandatory'))
			rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', fsn)])
			print('rto_id::::::::::::::::::::::::::', rto_id)
			if rto_id:
				raise UserError(_("Order ID "+o_i+' with FSN '+fsn+' in line '+str(count)+' is already exist in RTO Order'))

			product_id = fsn_id[0].product_id.default_code
			# print('product_id in import_rto method::::::::::::::::::::::::::', product_id)
			# print('fsn id  in import_rto method::::::::::::::::::::::::::', fsn_id[0])
			inv_id = self.original_order(o_i, product_id, count)
			# print('inv_id in rto import::::::::::::::::::::::::::', inv_id)
			# print('order_id in rto import::::::::::::::::::::::::::', o_i)
			# print('product_id in rto import::::::::::::::::::::::::::', product_id)
			# if inv_id != 0:
			# 	inv_line_ids = self.env['account.move.line'].search([('move_id', '=', inv_id), ('sku_name', '=', product_id)])
			# 	if not inv_line_ids:
			# 		raise UserError(_("The product of ASIN "+asin+' in line '+str(count)+' is not in order id '+o_i))
			qty = int(row[headers['Quantity']].strip())
			if qty < 1:
				raise UserError(_("Quantity must be at least one in line "+str(count)))
			# fc = row[headers['Warehouse ID']].strip()
			# if fc not in warehouse_code:
			# 	raise Warning(_("Warehouse ID "+fc+' is not found. '+' in line '+str(count)+'--in order-id '+o_i))
			# print("------------------count--------------", count)
			# count+=1
		print("--------------------complete-------------------")
		#----------------------------------------------------order-create----------------------------------------------------
		data_file.seek(0)
		headers = {}
		for row in reader:
			col_count = 0
			for col in row:
				headers[col] = col_count
				col_count = col_count + 1
			break;
		# print("------------headers------", headers)
		count =2
		for row in reader:
			o_i = row[headers['Order ID']].strip()
			rto_no = row[headers['RTO No']].strip()
			asin = row[headers['FSN']].strip()
			sku_map_id = self.env['sku.mapping'].search([('id_number', '=', asin)])
			print("lllllllllllllllllllllskumap",sku_map_id)
			product_id = sku_map_id[0].product_id
			print("lllllllllllllllllllllskumap",product_id)
			inv_id = self.original_order(o_i, product_id.default_code, count)
			rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', fsn), ('state', '=', 'draft')])

			# product_sku_code = row[headers['Product SKU Code']].strip()
			# sku_map_id = self.env['sku.mapping'].search([('default_code', '=', product_sku_code)])
			# product_id = sku_map_id[0].product_id
			# inv_id = self.original_order(o_i, product_id.default_code, count)
			# rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', product_sku_code), ('state', '=', 'draft')])

			# print("--------------wh-----", self.env['stock.warehouse'].search([('code', '=', row[headers['Warehouse ID']].strip())]))
			# print("--------------wh--id---", self.env['stock.warehouse'].search([('code', '=', row[headers['Warehouse ID']].strip())]).id)
			
			if not rto_id:
				vals={
					'return_o_no': rto_no,
					'return_date': datetime.strptime(row[headers['Return Date']].strip(), "%d/%m/%Y").date(),
					'portal_order_id': row[headers['Order ID']].strip(),
					'product_product_id': product_id.id,
					'asin': asin,
					'quntity': int(row[headers['Quantity']].strip()),
					'warehouse_id': self.env['stock.warehouse'].search([('code', '=', row[headers['Warehouse ID']].strip())]).id,
					'return_reason': row[headers['RTO Reason']].strip(),
					'month_of_return': self.month_of_return,
				}
				if inv_id == 0:
					pass
				else:
					invoice_line_id = self.env['account.move.line'].search([('move_id', '=', inv_id), ('sku_name', '=', product_id.default_code)])
					# vals['sale_order_id'] =  inv_id[0].so_id.id
					# vals['invoice_order_id'] = inv_id[0].id
					for line in invoice_line_id:
						print("--------------------line2222",line)
						vals['invoice_line_id']= line.id
					#print('------vals----------', vals['invoice_line_id'])
					# vals['odoo_order_b2b'] = inv_id[0].invoice_number_b2b
					# vals['odoo_order_b2c'] = inv_id[0].invoice_number
					# vals['from_warehouse_id'] = inv_id[0].warehouse_id.id
				# print("------vals-----", vals)
				order_create = self.env['return.order'].create(vals)
				# print("------------------order_create----------", order_create)
			else:
				# print("------------------rto_id[0]----------", rto_id[0])
				# print("------------------rto_id[0].quntity----------", rto_id[0].quntity)
				# print("------------------row[headers['Quantity']].strip()----------", row[headers['Quantity']].strip())
				qty1 = rto_id[0].quntity
				# print("------------qty1-----", qty1)
				# print("------------qty1--t---", type(qty1))
				qty2 = int(row[headers['Quantity']].strip())
				# print("------------qty2-----", qty2)
				# print("------------qty2---t--", type(qty2))
				qty3 = qty1+qty2
				# print("------------qty3-----", qty3)
				# print("------------qty3---t--", type(qty3))
				qty = rto_id[0].quntity+int(row[headers['Quantity']].strip())
				# print("---------------qty-----------------", qty)
				# print("---------------qty------------t------", type(qty))
				rto_id[0].update({'quntity': qty})
				print("------------------order_update----------")
			print("--------else----------count----------", count)
			count+=1


# for Other Portal 


	# def import_rto_other_portal(self):
	# 	print('---------RTO------')
	# 	f = base64.b64decode(self.return_order_file)
	# 	data_file = io.StringIO(f.decode("utf-8"))
	# 	reader = csv.reader(data_file, delimiter=',')
	# 	headers = {}
	# 	for row in reader:
	# 		col_count = 0
	# 		for col in row:
	# 			headers[col] = col_count
	# 			col_count = col_count + 1
	# 		break;
	# 	# print("------------headers------", headers)
	# 	#----------------------------------------------------one-time-check----------------------------------------------------
	# 	count =1
	# 	p_r_d = ''
	# 	for row in reader:
	# 		count+=1
	# 		r_d = datetime.strptime(row[headers['Return Date']].strip(), "%d/%m/%Y").date()
	# 		if not p_r_d:
	# 			p_r_d = r_d
	# 			continue;
	# 		if p_r_d and p_r_d > r_d:
	# 			raise Warning(_("Return Date must be in increasing order."))
	# 		else:
	# 			p_r_d = r_d
	# 		# if count >= 4:
	# 		#     break
	# 		# print("------------break------")
	# 	#----------------------------------------------------check-order----------------------------------------------------
	# 	data_file.seek(0)
	# 	headers = {}
	# 	for row in reader:
	# 		col_count = 0
	# 		for col in row:
	# 			headers[col] = col_count
	# 			col_count = col_count + 1
	# 		break;
	# 	count =2
	# 	print("------------------count--------------", count)
	# 	print("------------headers------", headers)
	# 	warehouse_ids = self.env['stock.warehouse'].search([])
	# 	warehouse_code = [k.code for k in warehouse_ids]
	# 	for row in reader:
	# 		rto_no = row[headers['RTO No']].strip()
	# 		rto_no_id = self.env['return.order'].search([('return_o_no', '=', rto_no)])
	# 		if rto_no_id:
	# 			raise UserError(_("RTO No "+rto_no+' in line '+str(count)+' is already exist in RTO Order'))
		

	# 		fsn = row[headers['sku']].strip()
	# 		if not fsn:
	# 			raise UserError(_("sku "+sku+' in line '+str(count)+' is mandatory'))
	# 		fsn_id = self.env['product.product'].search([('default_code', '=', fsn)])
	# 		print('*******************************************************', fsn_id)
	# 		if not fsn_id:
	# 			raise UserError(_("sku "+sku+' in line '+str(count)+' is not found. update in Product'))
	# 		o_i = row[headers['Order ID']].strip()
	# 		print('o_i::::::::::::::::::::::::::', o_i)
	# 		if not o_i:
	# 			raise UserError(_("Order ID "+o_i+' in line '+str(count)+' is mandatory'))
	# 		rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', fsn)])
	# 		print('rto_id::::::::::::::::::::::::::', rto_id)
	# 		if rto_id:
	# 			raise UserError(_("Order ID "+o_i+' with FSN '+fsn+' in line '+str(count)+' is already exist in RTO Order'))

	# 		product_id = fsn_id[0].default_code
	# 		# print('product_id in import_rto method::::::::::::::::::::::::::', product_id)
	# 		# print('fsn id  in import_rto method::::::::::::::::::::::::::', fsn_id[0])
	# 		inv_id = self.original_order(o_i, product_id, count)
	# 		# print('inv_id in rto import::::::::::::::::::::::::::', inv_id)
	# 		# print('order_id in rto import::::::::::::::::::::::::::', o_i)
	# 		# print('product_id in rto import::::::::::::::::::::::::::', product_id)
	# 		# if inv_id != 0:
	# 		# 	inv_line_ids = self.env['account.move.line'].search([('move_id', '=', inv_id), ('sku_name', '=', product_id)])
	# 		# 	if not inv_line_ids:
	# 		# 		raise UserError(_("The product of ASIN "+asin+' in line '+str(count)+' is not in order id '+o_i))
	# 		qty = int(row[headers['Quantity']].strip())
	# 		if qty < 1:
	# 			raise UserError(_("Quantity must be at least one in line "+str(count)))
	# 		# fc = row[headers['Warehouse ID']].strip()
	# 		# if fc not in warehouse_code:
	# 		# 	raise Warning(_("Warehouse ID "+fc+' is not found. '+' in line '+str(count)+'--in order-id '+o_i))
	# 		# print("------------------count--------------", count)
	# 		# count+=1
	# 	print("--------------------complete-------------------")
	# 	#----------------------------------------------------order-create----------------------------------------------------
	# 	data_file.seek(0)
	# 	headers = {}
	# 	for row in reader:
	# 		col_count = 0
	# 		for col in row:
	# 			headers[col] = col_count
	# 			col_count = col_count + 1
	# 		break;
	# 	# print("------------headers------", headers)
	# 	count =2
	# 	for row in reader:
	# 		o_i = row[headers['Order ID']].strip()
	# 		rto_no = row[headers['RTO No']].strip()
	# 		asin = row[headers['sku']].strip()
	# 		sku_map_id = self.env['product.product'].search([('default_code', '=', asin)])
	# 		print("lllllllllllllllllllllskumap",sku_map_id)
	# 		product_id = sku_map_id[0].id
	# 		print("lllllllllllllllllllllproduct_id",product_id)
	# 		inv_id = self.original_order(o_i, product_id, count)
	# 		rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', fsn), ('state', '=', 'draft')])

	# 		# product_sku_code = row[headers['Product SKU Code']].strip()
	# 		# sku_map_id = self.env['sku.mapping'].search([('default_code', '=', product_sku_code)])
	# 		# product_id = sku_map_id[0].product_id
	# 		# inv_id = self.original_order(o_i, product_id.default_code, count)
	# 		# rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', product_sku_code), ('state', '=', 'draft')])

	# 		# print("--------------wh-----", self.env['stock.warehouse'].search([('code', '=', row[headers['Warehouse ID']].strip())]))
	# 		# print("--------------wh--id---", self.env['stock.warehouse'].search([('code', '=', row[headers['Warehouse ID']].strip())]).id)
			
	# 		if not rto_id:
	# 			vals={
	# 				'return_o_no': rto_no,
	# 				'return_date': datetime.strptime(row[headers['Return Date']].strip(), "%d/%m/%Y").date(),
	# 				'portal_order_id': row[headers['Order ID']].strip(),
	# 				'product_product_id': product_id.id,
	# 				'asin': asin,
	# 				'quntity': int(row[headers['Quantity']].strip()),
	# 				'warehouse_id': self.env['stock.warehouse'].search([('code', '=', row[headers['Warehouse ID']].strip())]).id,
	# 				'return_reason': row[headers['RTO Reason']].strip(),
	# 				'month_of_return': self.month_of_return,
	# 			}
	# 			if inv_id == 0:
	# 				pass
	# 			else:
	# 				invoice_line_id = self.env['account.move.line'].search([('move_id', '=', inv_id),('sku_name', '=', product_id.id)])
	# 				# vals['sale_order_id'] =  inv_id[0].so_id.id
	# 				# vals['invoice_order_id'] = inv_id[0].id
	# 				for line in invoice_line_id:
	# 					vals['invoice_line_id']= line.id
	# 				#print('------vals----------', vals['invoice_line_id'])
	# 				# vals['odoo_order_b2b'] = inv_id[0].invoice_number_b2b
	# 				# vals['odoo_order_b2c'] = inv_id[0].invoice_number
	# 				# vals['from_warehouse_id'] = inv_id[0].warehouse_id.id
	# 			# print("------vals-----", vals)
	# 			order_create = self.env['return.order'].create(vals)
	# 			# print("------------------order_create----------", order_create)
	# 		else:
	# 			# print("------------------rto_id[0]----------", rto_id[0])
	# 			# print("------------------rto_id[0].quntity----------", rto_id[0].quntity)
	# 			# print("------------------row[headers['Quantity']].strip()----------", row[headers['Quantity']].strip())
	# 			qty1 = rto_id[0].quntity
	# 			# print("------------qty1-----", qty1)
	# 			# print("------------qty1--t---", type(qty1))
	# 			qty2 = int(row[headers['Quantity']].strip())
	# 			# print("------------qty2-----", qty2)
	# 			# print("------------qty2---t--", type(qty2))
	# 			qty3 = qty1+qty2
	# 			# print("------------qty3-----", qty3)
	# 			# print("------------qty3---t--", type(qty3))
	# 			qty = rto_id[0].quntity+int(row[headers['Quantity']].strip())
	# 			# print("---------------qty-----------------", qty)
	# 			# print("---------------qty------------t------", type(qty))
	# 			rto_id[0].update({'quntity': qty})
	# 			print("------------------order_update----------")
	# 		print("--------else----------count----------", count)
	# 		count+=1



	# def import_rto(self):
	# 	print('---------RTO------')
	# 	f = base64.b64decode(self.return_order_file)
	# 	data_file = io.StringIO(f.decode("utf-8"))
	# 	reader = csv.reader(data_file, delimiter=',')
	# 	headers = {}
	# 	for row in reader:
	# 		col_count = 0
	# 		for col in row:
	# 			headers[col] = col_count
	# 			col_count = col_count + 1
	# 		break;
	# 	# print("------------headers------", headers)
	# 	#----------------------------------------------------one-time-check----------------------------------------------------
	# 	count =1
	# 	p_r_d = ''
	# 	for row in reader:
	# 		count+=1
	# 		r_d = datetime.strptime(row[headers['Return Date']].strip(), "%d/%m/%Y").date()
	# 		if not p_r_d:
	# 			p_r_d = r_d
	# 			continue;
	# 		if p_r_d and p_r_d > r_d:
	# 			raise Warning(_("Return Date must be in increasing order."))
	# 		else:
	# 			p_r_d = r_d
	# 		# if count >= 4:
	# 		#     break
	# 		# print("------------break------")
	# 	#----------------------------------------------------check-order----------------------------------------------------
	# 	data_file.seek(0)
	# 	headers = {}
	# 	for row in reader:
	# 		col_count = 0
	# 		for col in row:
	# 			headers[col] = col_count
	# 			col_count = col_count + 1
	# 		break;
	# 	count =2
	# 	print("------------------count--------------", count)
	# 	print("------------headers------", headers)
	# 	warehouse_ids = self.env['stock.warehouse'].search([])
	# 	warehouse_code = [k.code for k in warehouse_ids]
	# 	for row in reader:
	# 		rto_no = row[headers['RTO No']].strip()
	# 		rto_no_id = self.env['return.order'].search([('return_o_no', '=', rto_no)])
	# 		product_name = row[headers['Product Name']].strip()
			
	# 		if rto_no_id:
	# 			raise UserError(_("RTO No "+rto_no+' in line '+str(count)+' is already exist in RTO Order'))
	# 		# inv_d = datetime.strptime(row[headers['purchase-date']].strip(), "%Y-%m-%dT%H:%M:%S%z").date()
	# 		# inv_d = datetime.strptime(row[headers['last-updated-date']].strip(), "%Y-%m-%dT%H:%M:%S%z").date()
	# 		# asin = row[headers['ASIN']].strip()
	# 		# if not asin:
	# 		# 	raise UserError(_("ASIN "+asin+' in line '+str(count)+' is mandatory'))
	# 		# asin_id = self.env['sku.mapping'].search([('id_number', '=', asin)])
	# 		# print('*******************************************************', asin_id)
	# 		# if not asin_id:
	# 		# 	raise UserError(_("ASIN "+asin+' in line '+str(count)+' is not found. update in SKU Mapping'))
	# 		# o_i = row[headers['Order ID']].strip()
	# 		# print('o_i::::::::::::::::::::::::::', o_i)
	# 		# if not o_i:
	# 		# 	raise UserError(_("Order ID "+o_i+' in line '+str(count)+' is mandatory'))
	# 		# rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', asin)])
	# 		# print('rto_id::::::::::::::::::::::::::', rto_id)
	# 		# if rto_id:
	# 		# 	raise UserError(_("Order ID "+o_i+' with ASIN '+asin+' in line '+str(count)+' is already exist in RTO Order'))


	# 		fsn = row[headers['FSN']].strip()
	# 		if not fsn:
	# 			raise UserError(_("FSN "+fsn+' in line '+str(count)+' is mandatory'))
	# 		fsn_id = self.env['sku.mapping'].search([('id_number', '=', fsn)])
	# 		print('fsn............................', fsn_id)
	# 		if not fsn_id:
	# 			raise UserError(_("FSN "+fsn+' in line '+str(count)+' is not found. update in SKU Mapping'))
	# 		o_i = row[headers['Order ID']].strip()
	# 		print('order_id.......................', o_i)
	# 		if not o_i:
	# 			raise UserError(_("Order ID "+o_i+' in line '+str(count)+' is mandatory'))
	# 		rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', fsn)])
	# 		print('rto_id::::::::::::::::::::::::::', rto_id)
	# 		if rto_id:
	# 			raise UserError(_("Order ID "+o_i+' with FSN '+fsn+' in line '+str(count)+' is already exist in RTO Order'))


	# 		# product_sku_code = row[headers['Product SKU Code']].strip()
			
	# 		# if not product_sku_code:
	# 		# 	raise UserError(_("Product SKU Code "+product_sku_code+' in line '+str(count)+' is mandatory'))
	# 		# product_sku_id = self.env['sku.mapping'].search([('default_code', '=', product_sku_code)])
	# 		# print('*******************************************************', product_sku_code)
	# 		# if not product_sku_code:
	# 		# 	raise UserError(_("Product SKU Code "+product_sku_code+' in line '+str(count)+' is not found. update in SKU Mapping'))
	# 		# o_i = row[headers['Order ID']].strip()
	# 		# print('o_i::::::::::::::::::::::::::', o_i)
	# 		# if not o_i:
	# 		# 	raise UserError(_("Order ID "+o_i+' in line '+str(count)+' is mandatory'))
	# 		# rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', product_sku_code)])
	# 		# print('rto_id::::::::::::::::::::::::::', rto_id)
	# 		# if rto_id:
	# 		# 	raise UserError(_("Order ID "+o_i+' with Product SKU Code '+product_sku_code+' in line '+str(count)+' is already exist in RTO Order'))




	# 		# inv_id = self.env['account.move'].search([('order_id', '=', o_i)])
	# 		# if not inv_id:
	# 		# 	raise UserError(_("Order ID "+o_i+' in line '+str(count)+' is not already exist'))
	# 		# if inv_id and inv_id[0].is_replacement == True:
	# 		# 	inv_rpl_id = self.env['account.move'].search([('order_id', '=', inv_id[0].original_order_id)])
	# 		# 	if not inv_rpl_id:
	# 		# 		raise UserError(_("Order ID "+o_i+' in line '+str(count)+' as replacement order id of original order id of '+inv_id[0].original_order_id+'is not already exist'))
	# 		# 	if inv_rpl_id and inv_rpl_id[0].is_replacement == True:
	# 		# 		inv_rpl2_id = self.env['account.move'].search([('order_id', '=', inv_rpl_id[0].original_order_id)])
	# 		# 		if not inv_rpl2_id:
	# 		# 			raise UserError(_("Order ID "+o_i+' in line '+str(count)+' as replacement order id of original order id of '+inv_rpl_id[0].original_order_id+'is not already exist'))	

	# 		# product_id = fsn_id[0].product_id.default_code
	# 		# # print('product_id::::::::::::::::::::::::::', product_id)
	# 		# inv_id = self.original_order(o_i, product_id, count)
	# 		# print('inv_id::::::::::::::::::::::::::', inv_id)
	# 		# if inv_id != 0:
	# 		# 	inv_line_ids = self.env['account.move.line'].search([('move_id', '=', inv_id), ('sku_name', '=', product_id)])
	# 		# 	if not inv_line_ids:
	# 		# 		raise UserError(_("The product of ASIN "+asin+' in line '+str(count)+' is not in order id '+o_i))
	# 		qty = int(row[headers['Quantity']].strip())
	# 		if qty < 1:
	# 			raise UserError(_("Quantity must be at least one in line "+str(count)))
	# 		# fc = row[headers['Warehouse ID']].strip()
	# 		# if fc not in warehouse_code:
	# 		# 	raise Warning(_("Warehouse ID "+fc+' is not found. '+' in line '+str(count)+'--in order-id '+o_i))
	# 		# print("------------------count--------------", count)
	# 		# count+=1
	# 	print("--------------------complete-------------------")
	# 	#----------------------------------------------------order-create----------------------------------------------------
	# 	data_file.seek(0)
	# 	headers = {}
	# 	for row in reader:
	# 		col_count = 0
	# 		for col in row:
	# 			headers[col] = col_count
	# 			col_count = col_count + 1
	# 		break;
	# 	# print("------------headers------", headers)
	# 	count =2
	# 	for row in reader:
	# 		o_i = row[headers['Order ID']].strip()
	# 		rto_no = row[headers['RTO No']].strip()
	# 		amount = row[headers['Amount']].strip()
	# 		# original_inv_id = ''
	# 		# inv_id = self.env['account.move'].search([('order_id', '=', o_i)])
	# 		# original_inv_id = inv_id
	# 		# inv_id = self.env['account.move'].search([('order_id', '=', o_i)])
	# 		# if not inv_id:
	# 		# 	raise UserError(_("Order ID "+o_i+' in line '+str(count)+' is not already exist'))
	# 		# if inv_id and inv_id[0].is_replacement == True:
	# 		# 	inv_rpl_id = self.env['account.move'].search([('order_id', '=', inv_id[0].original_order_id)])
	# 		# 	if not inv_rpl_id:
	# 		# 		raise UserError(_("Order ID "+o_i+' in line '+str(count)+' as replacement order id of original order id of '+inv_id[0].original_order_id+'is not already exist'))
	# 		# 	if inv_rpl_id and inv_rpl_id[0].is_replacement == True:
	# 		# 		inv_rpl2_id = self.env['account.move'].search([('order_id', '=', inv_rpl_id[0].original_order_id)])
	# 		# 		if not inv_rpl2_id:
	# 		# 			raise UserError(_("Order ID "+o_i+' in line '+str(count)+' as replacement order id of original order id of '+inv_rpl_id[0].original_order_id+'is not already exist'))	
	# 		# 	original_inv_id = inv_id
	# 		# original_inv_id = inv_id	
	# 		asin = row[headers['FSN']].strip()
	# 		# sku_map_id = self.env['sku.mapping'].search([('id_number', '=', fsn)])
	# 		# product_id = sku_map_id[0].product_id
	# 		# inv_id = self.original_order(o_i, product_id.default_code, count)
	# 		# print("inv_id::::::::::::::::::::",inv_id)
	# 		rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', fsn), ('state', '=', 'draft')])

	# 		# product_sku_code = row[headers['Product SKU Code']].strip()
	# 		# sku_map_id = self.env['sku.mapping'].search([('default_code', '=', product_sku_code)])
	# 		# product_id = sku_map_id[0].product_id
	# 		# inv_id = self.original_order(o_i, product_id.default_code, count)
	# 		# rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', product_sku_code), ('state', '=', 'draft')])

	# 		# print("--------------wh-----", self.env['stock.warehouse'].search([('code', '=', row[headers['Warehouse ID']].strip())]))
	# 		# print("--------------wh--id---", self.env['stock.warehouse'].search([('code', '=', row[headers['Warehouse ID']].strip())]).id)
			
	# 		if not rto_id:
	# 			vals={
	# 				'return_o_no': rto_no,
	# 				'return_date': datetime.strptime(row[headers['Return Date']].strip(), "%d/%m/%Y").date(),
	# 				'portal_order_id': row[headers['Order ID']].strip(),
	# 				'default_code': row[headers['Product Name']].strip(),
	# 				'asin': asin,
	# 				'quntity': int(row[headers['Quantity']].strip()),
	# 				'warehouse_id': self.env['stock.warehouse'].search([('code', '=', row[headers['Warehouse ID']].strip())]).id,
	# 				'return_reason': row[headers['RTO Reason']].strip(),
	# 				'month_of_return': self.month_of_return,
	# 				'price_unit': float(amount)
	# 			}
	# 			print("vals.................",vals)
	# 			# if inv_id == 0:
	# 			# 	pass
	# 			# else:
	# 			# 	invoice_line_id = self.env['account.move.line'].search([('move_id', '=', inv_id), ('sku_name', '=', product_id.default_code)])
	# 			# 	# vals['sale_order_id'] =  inv_id[0].so_id.id
	# 			# 	# vals['invoice_order_id'] = inv_id[0].id
	# 			# 	for line in invoice_line_id:
	# 			# 		vals['invoice_line_id']= line.id
	# 				# print('------vals----------', vals['invoice_line_id'])
	# 				# vals['odoo_order_b2b'] = inv_id[0].invoice_number_b2b
	# 				# vals['odoo_order_b2c'] = inv_id[0].invoice_number
	# 				# vals['from_warehouse_id'] = inv_id[0].warehouse_id.id
	# 			# print("------vals-----", vals)
	# 			order_create = self.env['return.order'].create(vals)
	# 			# print("------------------order_create----------", order_create)
	# 		else:
	# 			# print("------------------rto_id[0]----------", rto_id[0])
	# 			# print("------------------rto_id[0].quntity----------", rto_id[0].quntity)
	# 			# print("------------------row[headers['Quantity']].strip()----------", row[headers['Quantity']].strip())
	# 			qty1 = rto_id[0].quntity
	# 			# print("------------qty1-----", qty1)
	# 			# print("------------qty1--t---", type(qty1))
	# 			qty2 = int(row[headers['Quantity']].strip())
	# 			# print("------------qty2-----", qty2)
	# 			# print("------------qty2---t--", type(qty2))
	# 			qty3 = qty1+qty2
	# 			# print("------------qty3-----", qty3)
	# 			# print("------------qty3---t--", type(qty3))
	# 			qty = rto_id[0].quntity+int(row[headers['Quantity']].strip())
	# 			# print("---------------qty-----------------", qty)
	# 			# print("---------------qty------------t------", type(qty))
	# 			rto_id[0].update({'quntity': qty})
	# 			print("------------------order_update----------")
	# 			print("--------else----------count----------", count)
	# 		count+=1



		
	# def import_rto(self):
	# 	print('---------RTO------')
	# 	f = base64.b64decode(self.return_order_file)
	# 	data_file = io.StringIO(f.decode("utf-8"))
	# 	reader = csv.reader(data_file, delimiter=',')
	# 	headers = {}
	# 	for row in reader:
	# 		col_count = 0
	# 		for col in row:
	# 			headers[col] = col_count
	# 			col_count = col_count + 1
	# 		break;
	# 	# print("------------headers------", headers)
	# 	#----------------------------------------------------one-time-check----------------------------------------------------
	# 	count =1
	# 	p_r_d = ''
	# 	for row in reader:
	# 		count+=1
	# 		r_d = datetime.strptime(row[headers['Return Date']].strip(), "%d/%m/%Y").date()
	# 		if not p_r_d:
	# 			p_r_d = r_d
	# 			continue;
	# 		if p_r_d and p_r_d > r_d:
	# 			raise Warning(_("Return Date must be in increasing order."))
	# 		else:
	# 			p_r_d = r_d
	# 		# if count >= 4:
	# 		#     break
	# 		# print("------------break------")
	# 	#----------------------------------------------------check-order----------------------------------------------------
	# 	data_file.seek(0)
	# 	headers = {}
	# 	for row in reader:
	# 		col_count = 0
	# 		for col in row:
	# 			headers[col] = col_count
	# 			col_count = col_count + 1
	# 		break;
	# 	count =2
	# 	print("------------------count--------------", count)
	# 	print("------------headers------", headers)
	# 	warehouse_ids = self.env['stock.warehouse'].search([])
	# 	warehouse_code = [k.code for k in warehouse_ids]
	# 	for row in reader:
	# 		rto_no = row[headers['RTO No']].strip()
	# 		rto_no_id = self.env['return.order'].search([('return_o_no', '=', rto_no)])
	# 		if rto_no_id:
	# 			raise UserError(_("RTO No "+rto_no+' in line '+str(count)+' is already exist in RTO Order'))
	# 		# inv_d = datetime.strptime(row[headers['purchase-date']].strip(), "%Y-%m-%dT%H:%M:%S%z").date()
	# 		# inv_d = datetime.strptime(row[headers['last-updated-date']].strip(), "%Y-%m-%dT%H:%M:%S%z").date()
	# 		# asin = row[headers['ASIN']].strip()
	# 		# if not asin:
	# 		# 	raise UserError(_("ASIN "+asin+' in line '+str(count)+' is mandatory'))
	# 		# asin_id = self.env['sku.mapping'].search([('id_number', '=', asin)])
	# 		# print('*******************************************************', asin_id)
	# 		# if not asin_id:
	# 		# 	raise UserError(_("ASIN "+asin+' in line '+str(count)+' is not found. update in SKU Mapping'))
	# 		# o_i = row[headers['Order ID']].strip()
	# 		# print('o_i::::::::::::::::::::::::::', o_i)
	# 		# if not o_i:
	# 		# 	raise UserError(_("Order ID "+o_i+' in line '+str(count)+' is mandatory'))
	# 		# rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', asin)])
	# 		# print('rto_id::::::::::::::::::::::::::', rto_id)
	# 		# if rto_id:
	# 		# 	raise UserError(_("Order ID "+o_i+' with ASIN '+asin+' in line '+str(count)+' is already exist in RTO Order'))


	# 		fsn = row[headers['FSN']].strip()
	# 		if not fsn:
	# 			raise UserError(_("FSN "+fsn+' in line '+str(count)+' is mandatory'))
	# 		fsn_id = self.env['sku.mapping'].search([('id_number', '=', fsn)])
	# 		print('*******************************************************', fsn_id)
	# 		if not fsn_id:
	# 			raise UserError(_("FSN "+fsn+' in line '+str(count)+' is not found. update in SKU Mapping'))
	# 		o_i = row[headers['Order ID']].strip()
	# 		print('o_i::::::::::::::::::::::::::', o_i)
	# 		if not o_i:
	# 			raise UserError(_("Order ID "+o_i+' in line '+str(count)+' is mandatory'))
	# 		rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', fsn)])
	# 		print('rto_id::::::::::::::::::::::::::', rto_id)
	# 		if rto_id:
	# 			raise UserError(_("Order ID "+o_i+' with FSN '+fsn+' in line '+str(count)+' is already exist in RTO Order'))


	# 		# product_sku_code = row[headers['Product SKU Code']].strip()
			
	# 		# if not product_sku_code:
	# 		# 	raise UserError(_("Product SKU Code "+product_sku_code+' in line '+str(count)+' is mandatory'))
	# 		# product_sku_id = self.env['sku.mapping'].search([('default_code', '=', product_sku_code)])
	# 		# print('*******************************************************', product_sku_code)
	# 		# if not product_sku_code:
	# 		# 	raise UserError(_("Product SKU Code "+product_sku_code+' in line '+str(count)+' is not found. update in SKU Mapping'))
	# 		# o_i = row[headers['Order ID']].strip()
	# 		# print('o_i::::::::::::::::::::::::::', o_i)
	# 		# if not o_i:
	# 		# 	raise UserError(_("Order ID "+o_i+' in line '+str(count)+' is mandatory'))
	# 		# rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', product_sku_code)])
	# 		# print('rto_id::::::::::::::::::::::::::', rto_id)
	# 		# if rto_id:
	# 		# 	raise UserError(_("Order ID "+o_i+' with Product SKU Code '+product_sku_code+' in line '+str(count)+' is already exist in RTO Order'))




	# 		# inv_id = self.env['account.move'].search([('order_id', '=', o_i)])
	# 		# if not inv_id:
	# 		# 	raise UserError(_("Order ID "+o_i+' in line '+str(count)+' is not already exist'))
	# 		# if inv_id and inv_id[0].is_replacement == True:
	# 		# 	inv_rpl_id = self.env['account.move'].search([('order_id', '=', inv_id[0].original_order_id)])
	# 		# 	if not inv_rpl_id:
	# 		# 		raise UserError(_("Order ID "+o_i+' in line '+str(count)+' as replacement order id of original order id of '+inv_id[0].original_order_id+'is not already exist'))
	# 		# 	if inv_rpl_id and inv_rpl_id[0].is_replacement == True:
	# 		# 		inv_rpl2_id = self.env['account.move'].search([('order_id', '=', inv_rpl_id[0].original_order_id)])
	# 		# 		if not inv_rpl2_id:
	# 		# 			raise UserError(_("Order ID "+o_i+' in line '+str(count)+' as replacement order id of original order id of '+inv_rpl_id[0].original_order_id+'is not already exist'))	

	# 		product_id = fsn_id[0].product_id.default_code
	# 		print('product_id::::::::::::::::::::::::::', product_id)
	# 		inv_id = self.original_order(o_i, product_id, count)
	# 		print('inv_id::::::::::::::::::::::::::', inv_id)
	# 		# if inv_id != 0:
	# 		# 	inv_line_ids = self.env['account.move.line'].search([('move_id', '=', inv_id), ('sku_name', '=', product_id)])
	# 		# 	if not inv_line_ids:
	# 		# 		raise UserError(_("The product of ASIN "+asin+' in line '+str(count)+' is not in order id '+o_i))
	# 		qty = int(row[headers['Quantity']].strip())
	# 		if qty < 1:
	# 			raise UserError(_("Quantity must be at least one in line "+str(count)))
	# 		# fc = row[headers['Warehouse ID']].strip()
	# 		# if fc not in warehouse_code:
	# 		# 	raise Warning(_("Warehouse ID "+fc+' is not found. '+' in line '+str(count)+'--in order-id '+o_i))
	# 		# print("------------------count--------------", count)
	# 		# count+=1
	# 	print("--------------------complete-------------------")
	# 	#----------------------------------------------------order-create----------------------------------------------------
	# 	data_file.seek(0)
	# 	headers = {}
	# 	for row in reader:
	# 		col_count = 0
	# 		for col in row:
	# 			headers[col] = col_count
	# 			col_count = col_count + 1
	# 		break;
	# 	# print("------------headers------", headers)
	# 	count =2
	# 	for row in reader:
	# 		o_i = row[headers['Order ID']].strip()
	# 		rto_no = row[headers['RTO No']].strip()
	# 		# original_inv_id = ''
	# 		# inv_id = self.env['account.move'].search([('order_id', '=', o_i)])
	# 		# original_inv_id = inv_id
	# 		# inv_id = self.env['account.move'].search([('order_id', '=', o_i)])
	# 		# if not inv_id:
	# 		# 	raise UserError(_("Order ID "+o_i+' in line '+str(count)+' is not already exist'))
	# 		# if inv_id and inv_id[0].is_replacement == True:
	# 		# 	inv_rpl_id = self.env['account.move'].search([('order_id', '=', inv_id[0].original_order_id)])
	# 		# 	if not inv_rpl_id:
	# 		# 		raise UserError(_("Order ID "+o_i+' in line '+str(count)+' as replacement order id of original order id of '+inv_id[0].original_order_id+'is not already exist'))
	# 		# 	if inv_rpl_id and inv_rpl_id[0].is_replacement == True:
	# 		# 		inv_rpl2_id = self.env['account.move'].search([('order_id', '=', inv_rpl_id[0].original_order_id)])
	# 		# 		if not inv_rpl2_id:
	# 		# 			raise UserError(_("Order ID "+o_i+' in line '+str(count)+' as replacement order id of original order id of '+inv_rpl_id[0].original_order_id+'is not already exist'))	
	# 		# 	original_inv_id = inv_id
	# 		# original_inv_id = inv_id	
	# 		asin = row[headers['FSN']].strip()
	# 		sku_map_id = self.env['sku.mapping'].search([('id_number', '=', fsn)])
	# 		product_id = sku_map_id[0].product_id
	# 		inv_id = self.original_order(o_i, product_id.default_code, count)
	# 		rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', fsn), ('state', '=', 'draft')])

	# 		# product_sku_code = row[headers['Product SKU Code']].strip()
	# 		# sku_map_id = self.env['sku.mapping'].search([('default_code', '=', product_sku_code)])
	# 		# product_id = sku_map_id[0].product_id
	# 		# inv_id = self.original_order(o_i, product_id.default_code, count)
	# 		# rto_id = self.env['return.order'].search([('portal_order_id', '=', o_i), ('asin', '=', product_sku_code), ('state', '=', 'draft')])

	# 		# print("--------------wh-----", self.env['stock.warehouse'].search([('code', '=', row[headers['Warehouse ID']].strip())]))
	# 		# print("--------------wh--id---", self.env['stock.warehouse'].search([('code', '=', row[headers['Warehouse ID']].strip())]).id)
			
	# 		if not rto_id:
	# 			vals={
	# 				'return_o_no': rto_no,
	# 				'return_date': datetime.strptime(row[headers['Return Date']].strip(), "%d/%m/%Y").date(),
	# 				'portal_order_id': row[headers['Order ID']].strip(),
	# 				'product_product_id': product_id.id,
	# 				'asin': asin,
	# 				'quntity': int(row[headers['Quantity']].strip()),
	# 				'warehouse_id': self.env['stock.warehouse'].search([('code', '=', row[headers['Warehouse ID']].strip())]).id,
	# 				'return_reason': row[headers['RTO Reason']].strip(),
	# 				'month_of_return': self.month_of_return,
	# 			}
	# 			if inv_id == 0:
	# 				pass
	# 			else:
	# 				invoice_line_id = self.env['account.move.line'].search([('move_id', '=', inv_id), ('sku_name', '=', product_id.default_code)])
	# 				# vals['sale_order_id'] =  inv_id[0].so_id.id
	# 				# vals['invoice_order_id'] = inv_id[0].id
	# 				for line in invoice_line_id:
	# 					vals['invoice_line_id']= line.id
	# 				#print('------vals----------', vals['invoice_line_id'])
	# 				# vals['odoo_order_b2b'] = inv_id[0].invoice_number_b2b
	# 				# vals['odoo_order_b2c'] = inv_id[0].invoice_number
	# 				# vals['from_warehouse_id'] = inv_id[0].warehouse_id.id
	# 			# print("------vals-----", vals)
	# 			order_create = self.env['return.order'].create(vals)
	# 			# print("------------------order_create----------", order_create)
	# 		else:
	# 			# print("------------------rto_id[0]----------", rto_id[0])
	# 			# print("------------------rto_id[0].quntity----------", rto_id[0].quntity)
	# 			# print("------------------row[headers['Quantity']].strip()----------", row[headers['Quantity']].strip())
	# 			qty1 = rto_id[0].quntity
	# 			# print("------------qty1-----", qty1)
	# 			# print("------------qty1--t---", type(qty1))
	# 			qty2 = int(row[headers['Quantity']].strip())
	# 			# print("------------qty2-----", qty2)
	# 			# print("------------qty2---t--", type(qty2))
	# 			qty3 = qty1+qty2
	# 			# print("------------qty3-----", qty3)
	# 			# print("------------qty3---t--", type(qty3))
	# 			qty = rto_id[0].quntity+int(row[headers['Quantity']].strip())
	# 			# print("---------------qty-----------------", qty)
	# 			# print("---------------qty------------t------", type(qty))
	# 			rto_id[0].update({'quntity': qty})
	# 			print("------------------order_update----------")
	# 		print("--------else----------count----------", count)
	# 		count+=1
