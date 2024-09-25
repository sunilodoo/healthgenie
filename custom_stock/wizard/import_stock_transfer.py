# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
# from openerp.tools.translate import _
# from openerp import tools, api
# from openerp import SUPERUSER_ID
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


class ImportWarehouse(models.TransientModel):
	_name = 'import.stock.transfer'
	_description = 'Import Warehouse'

	stock_transfer_file = fields.Binary(string='CSV File', help='File should be separated by comma (,) and quoted using Quote character (") ')
	
	
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
	
	
	
	def stock_transfer_check(self):
		f = base64.b64decode(self.stock_transfer_file)
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
		warehouse_ids = self.env['stock.warehouse'].search([])
		warehouse_code = [k.code for k in warehouse_ids]
		warehouse_gstin = [k.gstin for k in warehouse_ids]
		pool_pincode_state= self.env['pincode.state'].search([])
		print("------------warehouse_names------", warehouse_code)
		for row in reader:
			count = count+1
			ship_from_fc = row[headers['Ship From Fc']].strip()
			ship_to_fc = row[headers['Ship To Fc']].strip()
			gstin_of_receiver = row[headers['Gstin Of Receiver']].strip()
			gstin_of_supplier = row[headers['Gstin Of Supplier']].strip()
			ship_from_postal_code = row[headers['Ship From Postal Code']].strip()
			ship_to_postal_code = row[headers['Ship To Postal Code']].strip()
			asin = row[headers['Asin']].strip()
			hsn = row[headers['Hsn Code']].strip()
			if not ship_from_fc:
				raise Warning(_("Ship From Fc "+' is not '+' in line '+str(count)+ '--as '+row[headers['Transaction Id']].strip()))
			if ship_from_fc not in warehouse_code:
				raise Warning(_("Ship From Fc "+row[headers['Ship From Fc']].strip()+' in line '+str(count)+' is not found. '+ '--as '+row[headers['Ship From Fc']].strip()+'in Stock Warehouse'))
			if not ship_to_fc:
				raise Warning(_("Ship To Fc "+' is not '+' in line '+str(count)+ '--as '+row[headers['Transaction Id']].strip()))
			if ship_to_fc not in warehouse_code:
				raise Warning(_("Ship To Fc "+row[headers['Ship To Fc']].strip()+' in line '+str(count)+' is not found. '+ '--as '+row[headers['Ship To Fc']].strip()+'in Stock Warehouse'))
			if not gstin_of_receiver:
				raise Warning(_("Gstin Of Receiver "+' is not '+' in line '+str(count)+ '--as '))
			if gstin_of_receiver not in warehouse_gstin:
				raise Warning(_("Gstin Of Receiver "+row[headers['Ship To Fc']].strip()+' in line '+str(count)+' is not found. '+ '--as '+row[headers['Gstin Of Receiver']].strip()))
			if not gstin_of_supplier:
				raise Warning(_("Gstin Of Supplier "+' is not '+' in line '+str(count)+ '--as '))
			if gstin_of_supplier not in warehouse_gstin:
				raise Warning(_("Gstin Of Supplier "+row[headers['Ship From Fc']].strip()+' in line '+str(count)+' is not found. '+ '--as '+row[headers['Gstin Of Supplier']].strip()))

			if not ship_from_postal_code:
				raise Warning(_("Ship From Postal Code "+' is not '+' in line '+str(count)+ '--as '))
			if not self.env['pincode.state'].search([('name', '=', ship_from_postal_code)]):
				raise Warning(_("Ship From Postal Code "+ship_from_postal_code+' in line '+str(count)+' is not found. '+ '--as '+'in State Pincode'))
			if not ship_to_postal_code:
				raise Warning(_("Ship From Postal Code "+' is not '+' in line '+str(count)+ '--as '))
			if not self.env['pincode.state'].search([('name', '=', ship_to_postal_code)]):
				raise Warning(_("Ship From Postal Code "+ship_to_postal_code+' in line '+str(count)+' is not found. '+ '--as '+'in State Pincode'))
			if not asin:
				raise Warning(_("Asin "+' is not '+' in line '+str(count)))
			if not self.env['sku.mapping'].search([('portal_id_type', '=', 'asin'), ('id_number', '=', asin)]):
				raise Warning(_("Asin "+asin+' in line '+str(count)+' is not found. '+ '--as '+asin))
			print("-------------------hsn-----------------", hsn)
			# if not hsn:
			# 	print("-----------------not--1--hsn-----------------", hsn)
			# 	# raise Warning(_("Hsn Code "+' is not '+' in line '+str(count)+ '--as '))
			# if not self.env['product.product'].search([('l10n_in_hsn_code', '=', hsn)]):
			# 	print("-----------------not--2---hsn-----------------", hsn)
			# 	raise Warning(_("Hsn Code "+hsn+' in line '+str(count)+' is not found. '+ '--as '+hsn))
	def import_stock_transfer(self):
		# partner_pool = self.env['res.partner']
		# warehouse_pool = self.env['stock.warehouse']
		f = base64.b64decode(self.stock_transfer_file)
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
		already_order = ''
		already_order_id_s_p = ''
		s_p_ids = []
		already_order_id_s_t_s = ''
		already_order_id_s_t_p = ''
		for row in reader:
			# print("------------------------------date-------------------------", row[headers["Invoice Date"]].strip())
			quntity = float(row[headers["Quantity"]].strip())
			date = datetime.strptime(row[headers["Invoice Date"]].strip(), "%d/%m/%Y %H:%M")
			vals ={
				'gstin_of_receiver' : row[headers["Gstin Of Receiver"]].strip(),
				'month_of_stock_trns' : self.month_of_stock_trns,
				'trn_type' : row[headers["Transaction Type"]].strip(),
				'trans_id' : row[headers["Transaction Id"]].strip(),
				'ord_id' : row[headers["Order Id"]].strip(),
				'ship_from_city' : row[headers["Ship From City"]].strip(),
				'ship_from_state' : row[headers["Ship From State"]].strip(),
				'ship_from_country' : row[headers["Ship From Country"]].strip(),
				'ship_f_p_c' : row[headers["Ship From Postal Code"]].strip(),
				'ship_from_fc' : row[headers["Ship From Fc"]].strip(),
				'ship_to_fc' : row[headers["Ship To Fc"]].strip(),
				'ship_to_city' : row[headers["Ship To City"]].strip(),
				'ship_to_state' : row[headers["Ship To State"]].strip(),
				'ship_to_country' : row[headers["Ship To Country"]].strip(),
				'ship_to_p_c' : row[headers["Ship To Postal Code"]].strip(),
				'invoice_no' : row[headers["Invoice Number"]].strip(),
				'invoice_date' : date,
				# 'invoice_date' : datetime.strptime(row[headers["Invoice Date"]].strip(), "%d/%m/%Y, %H:%M:%S"),
				'invoice_vales' : float(row[headers["Invoice Value"]].strip()),
				'asin' : row[headers["Asin"]].strip(),
				'sku' : row[headers["Sku"]].strip(),
				'quntity' : quntity,
				'hsn_code' : row[headers["Hsn Code"]].strip(),
				'taxable_value' : row[headers["Taxable Value"]].strip(),
				'igst_rate' : row[headers["Igst Rate"]].strip(),
				'igst_amount' : row[headers["Igst Amount"]].strip(),
				'sgst_rate' : row[headers["Sgst Rate"]].strip(),
				'sgst_amount' : row[headers["Sgst Amount"]].strip(),
				'utgst_rate' : row[headers["Utgst Rate"]].strip(),
				'utgst_amount' : row[headers["Utgst Amount"]].strip(),
				'cgst_rate' : row[headers["Cgst Rate"]].strip(),
				'cgst_amount' : row[headers["Cgst Amount"]].strip(),
				'comp_c_r' : row[headers["Compensatory Cess Rate"]].strip(),
				'comp_c_a' : row[headers["Compensatory Cess Amount"]].strip(),
				'gstin_of_supplier' : row[headers["Gstin Of Supplier"]].strip(),
				'irn_no' : row[headers["Irn Number"]].strip(),
				'irn_f_s' : row[headers["Irn Filing Status"]].strip(),
				'irn_date' : row[headers["Irn Date"]].strip(),
				'irn_e_c' : row[headers["Irn Error Code"]].strip()
			}
			vals_pick_line ={}
			vals_sale_line ={
				'trans_id' : row[headers["Transaction Id"]].strip(),
				'invoice_no' : row[headers["Invoice Number"]].strip(),
				'quntity' : quntity,
				'invoice_vales' : float(row[headers["Invoice Value"]].strip()),
			}
			vals_purchase_line ={
				'trans_id' : row[headers["Transaction Id"]].strip(),
				'invoice_no' : row[headers["Invoice Number"]].strip(),
				'quntity' : quntity,
				'invoice_vales' : float(row[headers["Invoice Value"]].strip()),
			}
			asin = self.env['sku.mapping'].search([('portal_id_type', '=', 'asin'), ('id_number', '=', row[headers["Asin"]].strip())])
			if asin:
				# vals['asin'] = row[headers["Asin"]].strip()
				vals_sale_line['asin'] = asin[0].id_number
				vals_sale_line['sku'] = asin[0].name
				vals_sale_line['product_product_id'] = asin[0].product_id.id
				vals_pick_line['move_ids_without_package'] = [(0,0, {'product_id':asin[0].product_id.id, 'name': asin[0].product_id.name, 'product_uom_qty': quntity, 'product_uom': asin[0].product_id.uom_id, 'date': date.date()})]
				# vals_pick['move_ids_without_package'] = [(0,0, {'product_id':asin[0].product_id.id, 'name': asin[0].product_id.name, 'product_uom_qty': quntity, 'product_uom': asin[0].product_id.uom_id})]
				vals_purchase_line['asin'] = asin[0].id_number
				vals_purchase_line['sku'] = asin[0].name
				vals_purchase_line['product_product_id'] = asin[0].product_id.id
			else:
				raise Warning(_("Asin--------"+row[headers['Asin']].strip()+" is not found in line----"+str(count)))
			# print("----------------------vals_pick_line----------------", vals_pick_line)
			# print("----------------------vals_pick_line-----t-----------", type(vals_pick_line))
			o_i = row[headers["Order Id"]].strip()
			# print("----------------already_order---------------", already_order)
			# print("----------------o_i---------------", o_i)
			# print("-------------------------------")
			already_sts = self.env['stock.transfer.sale'].search([('ord_id', '=', o_i)])
			if not already_sts:
				# print("---------------if----------------", already_order)
				# print("---------------if----------------", o_i)
				already_order = o_i
				vals_pick ={
					'move_ids_without_package': vals_pick_line['move_ids_without_package']
				}
				vals_sale ={
					'month_of_stock_trns' : self.month_of_stock_trns,
					'ord_id' : row[headers["Order Id"]].strip(),
					'invoice_no' : row[headers["Invoice Number"]].strip(),
					'invoice_date' : datetime.strptime(row[headers["Invoice Date"]].strip(), "%d/%m/%Y %H:%M"),
					'stock_transfer_line' : [(0,0, vals_sale_line)]
				}
				vals_purchase ={
					'month_of_stock_trns' : self.month_of_stock_trns,
					'ord_id' : row[headers["Order Id"]].strip(),
					'invoice_no' : row[headers["Invoice Number"]].strip(),
					'invoice_date' : datetime.strptime(row[headers["Invoice Date"]].strip(), "%d/%m/%Y %H:%M"),
					'stock_transfer_line' : [(0,0, vals_purchase_line)]
				}
				trn_type = row[headers["Transaction Type"]].strip()
				if trn_type == 'FC_REMOVAL':
					vals['trn_type'] = 'fcr'
					vals_sale['trn_type'] = 'fcr'
					vals_sale['credit_note'] = True
					vals_purchase['trn_type'] = 'fcr'
					vals_purchase['debit_note'] = True
				elif trn_type == 'FC_REMOVAL-Cancel':
					vals['trn_type'] = 'fcrc'
				elif trn_type == 'FC_TRANSFER':
					vals['trn_type'] = 'fct'
					vals_sale['trn_type'] = 'fct'
					vals_purchase['trn_type'] = 'fct'
				gstin_of_receiver = self.env['stock.warehouse'].search([('code', '=', row[headers["Ship To Fc"]].strip())])
				if gstin_of_receiver:
					# vals['gstin_of_receiver'] = gstin_of_receiver.gstin
					# vals['ship_to_fc'] = gstin_of_receiver.code
					vals_pick['partner_id'] = gstin_of_receiver.partner_id.id
					vals_pick['location_dest_id'] = self.env['stock.location'].search([('complete_name', '=', gstin_of_receiver.code+'/Stock')]).id
					vals_sale['ship_to_fc'] = gstin_of_receiver.id
					vals_purchase['ship_to_fc'] = gstin_of_receiver.id
				else:
					raise Warning(_("Gstin Of Receiver--------"+row[headers['Gstin Of Receiver']].strip()+"---or---"+"Ship From Fc-------"+row[headers["Ship From Fc"]].strip()+" is not found in line----"+str(count)))
				gstin_of_supplier = self.env['stock.warehouse'].search([('code', '=', row[headers["Ship From Fc"]].strip())])
				if gstin_of_supplier:
					vals_pick['picking_type_id'] = self.env['stock.picking.type'].search([('name', '=', 'Internal Transfers'), ('warehouse_id', '=', gstin_of_supplier.id)]).id
					vals_pick['location_id'] = self.env['stock.location'].search([('complete_name', '=', gstin_of_supplier.code+'/Stock')]).id
					vals_sale['ship_from_fc'] = gstin_of_supplier.id
					vals_purchase['ship_from_fc'] = gstin_of_supplier.id
				else:
					raise Warning(_("Gstin Of Supplier--------"+row[headers['Gstin Of Supplier']].strip()+"---or---"+"Ship To Fc-------"+row[headers["Ship To Fc"]].strip()+" is not found in line ----"+str(count)))
				stock_t = self.env['stock.transfer'].create(vals)
				print("-----------------stock_t.id---", stock_t.id)
				if stock_t:
					if trn_type == 'FC_TRANSFER' or trn_type == 'FC_REMOVAL':
						stock_p = self.env['stock.picking'].create(vals_pick)
						# print("-----------------stock_p------", stock_p)
						s_p_ids.append(stock_p.id)
						# already_order_id_s_p = stock_p
						# print("-----------------already_order_id_s_p------", already_order_id_s_p)
						# stock_p_id = stock_p
						vals_sale['stock_transfer'] = stock_t.id
						vals_sale_line['stock_transfer'] = stock_t.id
						vals_sale['transfer_id_odoo'] = stock_p.id
						vals_purchase['stock_transfer'] = stock_t.id
						vals_purchase_line['stock_transfer'] = stock_t.id
						vals_purchase['transfer_id_odoo'] = stock_p.id
						stock_t_s = self.env['stock.transfer.sale'].create(vals_sale)
						vals_purchase['sale_invoice'] = stock_t_s.sale_invoice
						# already_order_id_s_t_s = stock_t_s
						stock_t_p = self.env['stock.transfer.purchase'].create(vals_purchase)
						# already_order_id_s_t_p = stock_t_p
						# if stock_p:
						# 	stock_p.action_confirm()
						# 	stock_p.action_assign()
						# 	# stml_id = self.env['stock.move.line'].search([('reference', '=', stock_p.name), ('product_uom_qty', '=', quntity)])
						# 	pml_ids = self.env['stock.move.line'].search([('picking_id', '=', stock_p.id), ('state', '=', 'assigned')])
						# 	for pml in pml_ids:
						# 		pml._onchange_qty_done_inherit()
						# 	stock_p.button_validate()
				count+=1
				print("---------------if---count------", count)
			else:
				already_stp = self.env['stock.transfer.purchase'].search([('ord_id', '=', o_i)])
				already_sp = already_sts.transfer_id_odoo
				print("------------------else--------count---", count)
				trn_type = row[headers["Transaction Type"]].strip()
				if trn_type == 'FC_REMOVAL':
					vals['trn_type'] = 'fcr'
				elif trn_type == 'FC_REMOVAL-Cancel':
					vals['trn_type'] = 'fcrc'
				elif trn_type == 'FC_TRANSFER':
					vals['trn_type'] = 'fct'
				stock_t = self.env['stock.transfer'].create(vals)
				if trn_type == 'FC_TRANSFER' or trn_type == 'FC_REMOVAL':
					vals_pick_line['move_ids_without_package'][0][2]['location_id'] = already_sp.location_id
					vals_pick_line['move_ids_without_package'][0][2]['location_dest_id'] = already_sp.location_dest_id
					# print("------------------------------&&&&&&&&&&&&&&&&&&--------------------vals_pick_line---------------------", vals_pick_line)
					already_sp.write(vals_pick_line)
					vals_sale_line['stock_transfer'] = stock_t.id
					vals_purchase_line['stock_transfer'] = stock_t.id
					# print("---------------------@@@@@@@@@@@@@2222------------")
					already_sts.write({'stock_transfer_line' : [(0,0, vals_sale_line)]})
					already_stp.write({'stock_transfer_line' : [(0,0, vals_purchase_line)]})
				count+=1
				print("------------------count------", count)
		# print("------------------s_p_ids------", s_p_ids)
		for sp_rec in s_p_ids:
			sp_id =  self.env['stock.picking'].search([('id', '=', sp_rec)])
			# print("------------------sp_id------", sp_id)
			sp_id.action_confirm()
			# print("------------------s_t_c----2--")
			sp_id.action_assign()
			# print("------------------s_t_c----3--")
			# stml_id = self.env['stock.move.line'].search([('reference', '=', stock_p.name), ('product_uom_qty', '=', quntity)])
			pml_ids = self.env['stock.move.line'].search([('picking_id', '=', sp_id.id), ('state', '=', 'assigned')])
			# print("------------------s_t_c----4--", pml_ids)
			for pml in pml_ids:
				# print("------------------s_t_c----5--")
				pml._onchange_qty_done_inherit()
				# print("------------------s_t_c----6--")
			sp_id.button_validate()
			# print("------------------s_t_c----7--")
		print("------------------complete--")