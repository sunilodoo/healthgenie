# -*- coding: utf-8 -*-
import base64
import io
import csv
import calendar
# from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
from odoo.exceptions import Warning

class SaleOrderReport(models.TransientModel):
    _name = "sale.order.import"
    _description = 'Sale Order Import'
    order_b2b_b2c = fields.Selection([('b2b', 'B2B'), ('b2c', 'B2C')], string="Order(B2B/B2C)", default=False, required=True)
    order_file = fields.Binary(string='Order CSV File', required=True, help='File should be separated by comma (,) and quoted using Quote character (")')

    def action_confirm_so(self):
        print("-----------action_confirm_so---------", self)
        action_confirm_so_draft=self.env['sale.order'].search([('state', '=', 'draft')], order='id asc')
        # action_confirm_so_draft=self.env['sale.order'].search([('state', '=', 'draft')], order='id asc')
        print("-----------action_confirm_so_draft------", action_confirm_so_draft)
        for soaf in action_confirm_so_draft:
            print("-----------------soaf$$$so--------------------", soaf.name)
            print("-----------------soaf--------------------", soaf.action_confirm())
            # break;
    def action_create_invoice_so(self):
        print("-----------action_create_invoice_so---------", self)
        so_to_inv_ids = self.env['sale.order'].search([('invoice_status', '=', 'to invoice')], order='id asc')
        print("-----------so_to_inv_ids------", so_to_inv_ids)
        for soci in so_to_inv_ids:
            print("-----------------soci--------------------", soci.name)
            print("-----------------soci--------------------", self.env['sale.order']._create_invoices())
            break;
    def delete_sale_order(self):
        print("---------------------------delete_sale_order--------------------------")
        som = self.env['sale.order'].search([])
        for rec1 in som:
            print("--------rec1.unlink()-------", rec1.unlink())
    def delete_sale_order_missing(self):
        soi = self.env['sale.order.missing'].search([])
        for rec2 in soi:
            print("--------rec2.unlink()-------", rec2.unlink())
        # s_p_ids = self.env['stock.picking'].search([('state', '=', 'assigned')], order='id asc')
        # for rec2 in s_p_ids:
        #     print("--------rec2.unlink()-------", rec2)
        #     print("--------rec2.unlink()-------", rec2.action_cancel())

    def states_sku_Warehouse_check(self):
        f = base64.b64decode(self.order_file)
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
        states_ids = self.env['res.country.state'].search([('country_id', '=', 104)])
        state_names = [i.name for i in states_ids]
        sku_ids = self.env['sku.mapping'].search([])
        sku_names = [j.name for j in sku_ids]
        warehouse_ids = self.env['stock.warehouse'].search([])
        warehouse_names = [k.name for k in warehouse_ids]
        print("------------state_name------", state_names)
        for row in reader:
            count = count+1
            if row[headers['State-shipping']].strip() not in state_names:
                print("--------------count-----------", )
                raise Warning(_("The State-shipping "+row[headers['State-shipping']].strip()+' is not found. '+' in line '+str(count)+ '--as '+row[headers['order-id']].strip()))
            if row[headers['sku-id']].strip() not in sku_names:
                raise Warning(_("The SKU_ID "+row[headers['sku-id']].strip()+' is not found. '+' in line '+str(count)+ '--as '+row[headers['order-id']].strip()))
            if row[headers['warehouse']].strip() not in warehouse_names:
                raise Warning(_("The Warehouse "+row[headers['warehouse']].strip()+' is not found. '+' in line '+str(count)+ '--as '+row[headers['order-id']].strip()))
            t_p = self.env['res.partner'].search([('name', '=', row[headers['sales-channel']].strip())])
            if not t_p:
                raise Warning(_("The Third Party "+row[headers['sales-channel']].strip()+' is not found. Please Create in Contects as Customer'))


    def do_import(self):
        f = base64.b64decode(self.order_file)
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
        already_order_id = ''
        already_so_id = ''

        if self.order_b2b_b2c == 'b2c':
            for row in reader:
                order_id = row[headers['order-id']].strip() if row[headers['order-id']].strip() else ''
                if order_id != already_order_id:
                    already_order_id = order_id
                    customer_vals ={
                        'name': row[headers['Customer-name-shipping']].strip(),
                        'street': row[headers['address-shipping']].strip(),
                        'city': row[headers['city-shipping']].strip(),
                        # 'state_id': self.env['res.country.state'].search([('name', '=', row[headers['State-shipping']]), ('country_id', '=', 104)])[0].id,
                        'zip': row[headers['pincode-shipping']].strip(),
                    }
                    state_ids = self.env['res.country.state'].search([('name', '=', row[headers['State-shipping']].strip()), ('country_id', '=', 104)])
                    if state_ids:
                        customer_vals['state_id'] =  state_ids[0].id
                        customer_vals['country_id'] =  104
                    else:
                        raise Warning(_("The State "+row[headers['State-shipping']].strip()+' is not found. Please Create state in Fed. state'))
                        # self.env['sale.order.missing'].create({'channel_name': row[headers['sales-channel']].strip(), 'order_no': order_id, 'sku_name': row[headers['sku-id']].strip(), 'reason': 'The State '+row[headers['State-shipping']].strip()+' is not found. Please Create state in Fed. state'})
                        # count = count+1
                        # print("---------------------count-------------------", count)
                        # continue
                    customer_id = self.env['res.partner'].create(customer_vals)
                    # d_o = datetime.strptime(row[headers['order-date']].strip(), "%d-%b-%y")
                    d_o = datetime.strptime(row[headers['order-date']].strip(), "%d/%m/%y")
                    o_d = datetime.strptime(row[headers['order-date']].strip(), "%d/%m/%y").date()
                    # inv_d = datetime.strptime(row[headers['Invoice Date']].strip(), "%d-%b-%y").date()
                    inv_d = datetime.strptime(row[headers['order-date']].strip(), "%d/%m/%y").date()
                    # inv_d = datetime.strptime(row[headers['Invoice Date']].strip(), "%d/%m/%y").date()
                    order_vals = {
                        'partner_id': customer_id.id,
                        'order_id': order_id,
                        'date_order': d_o,
                        'order_date': o_d,
                        'order_type': row[headers['Order type']].strip(),
                        'order_category': self.order_b2b_b2c,
                        'invoice_no': row[headers['Invoice No.']].strip(),
                        'invoice_date': inv_d,
                        # 'tracking_no': row[headers['tracking id']].strip(),
                        # 'delivery_partner_name': row[headers['Delivery partner']].strip()
                    }
                    t_p = self.env['res.partner'].search([('name', '=', row[headers['sales-channel']].strip())])
                    if t_p:
                        order_vals['third_party'] =  t_p[0].id
                    else:
                        raise Warning(_("The Third Party "+row[headers['sales-channel']].strip()+' is not found. Please Create in Contects as Customer'))
                    w_i = self.env['stock.warehouse'].search([('name', '=', row[headers['warehouse']].strip())])
                    if w_i:
                        order_vals['warehouse_id'] =  w_i[0].id
                    else:
                        raise Warning(_("The Warehouse "+row[headers['warehouse']].strip()+' is not found. Please Create in Inventory as Warehouse'))
                    sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['sku-id']].strip())])
                    if sk_id:
                        order_vals['order_line'] = [(0,0,{'product_id': sk_id[0].product_id.id, 'name': sk_id[0].product_id.name, 'sku_id': sk_id[0].id, 'sku_name': sk_id[0].default_code, 'product_uom_qty': row[headers['qty']].strip(), 'portal_price': float( row[headers['item-unit-price']].strip()), 'unit_shipping_charges': row[headers['unit-shipping-charges']].strip()})]
                    else:
                        raise Warning(_("The Product -----"+row[headers['product-name']].strip()+"----- has not been map with ---------"+row[headers['sku-id']].strip()+"----- please create SKU ID of product"))
                    order_create = self.env['sale.order'].create(order_vals)
                    already_so_id = order_create
                    print("------------------order_create-------------", order_create)
                    count = count+1
                    print("---------------------------count---------------------", count)
                else:
                    sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['sku-id']].strip())])
                    if sk_id:
                        order_write = already_so_id.write({'order_line': [(0,0,{'product_id': sk_id.product_id.id, 'name': sk_id.product_id.name, 'sku_id': sk_id.id, 'sku_name': sk_id.name, 'name': sk_id.product_id.name, 'product_uom_qty': row[headers['qty']].strip(), 'portal_price': float( row[headers['item-unit-price']].strip()), 'unit_shipping_charges': row[headers['unit-shipping-charges']].strip()})]})
                        print("-----------------order_write--------------", order_write)
                        count = count+1
                        print("-----------------else-------count----------", count)
                    else:
                        raise Warning(_("The Product -----"+row[headers['product-name']]+"----- has not been map with ---------"+row[headers['sku-id']].strip()+"----- please create SKU ID of product"))

        if self.order_b2b_b2c == 'b2b':
            print("-----------------yes-------b2b----")
            already_order_id = ''
            already_so_id = ''
            for row in reader:
                order_id = row[headers['PO']].strip() if row[headers['PO']].strip() else ''
                if order_id is not already_order_id:
                    already_order_id = order_id
                    d_o = datetime.strptime(row[headers['PO Date']].strip(), "%d/%m/%Y")
                    order_vals = {
                        'hg_party_id': row[headers['HG Party ID']].strip(),
                        'order_id': order_id,
                        'date_order': d_o,
                        'order_type': row[headers['Third party']].strip(),
                        'order_category': self.order_b2b_b2c
                    }
                    t_p = self.env['res.partner'].search([('name', '=', row[headers['Third party']].strip())])
                    if t_p:
                        order_vals['third_party'] =  t_p[0].id
                        order_vals['partner_id'] =  t_p[0].id
                    else:
                        raise Warning(_("The Third Party "+row[headers['Third party']].strip()+' is not found. Please Create in Contects as Customer'))
                    w_i = self.env['stock.warehouse'].search([('fs', '=', row[headers['Warehouse']].strip())])
                    if w_i:
                        order_vals['warehouse_id'] =  w_i[0].id
                    else:
                        raise Warning(_("The Warehouse "+row[headers['Warehouse']].strip()+' is not found. Please Create in Inventory as Warehouse'))
                    sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['SKU']].strip())])
                    if sk_id:
                        order_vals['order_line'] = [(0,0,{'product_id': sk_id[0].product_id.id, 'name': sk_id[0].product_id.name, 'sku_id': sk_id[0].id, 'sku_name': sk_id[0].name, 'name': sk_id[0].product_id.name, 'product_uom_qty': row[headers['Quantity']].strip(), 'price_unit': row[headers['Cost']].strip()})]
                    else:
                        # self.env['sale.order.missing'].create({'channel_name': row[headers['sales-channel']], 'order_no': order_id, 'sku_name': row[headers['sku-id']], })
                        raise Warning(_("The Product -----"+row[headers['Title']].strip()+"----- has not been map with ---------"+row[headers['SKU']].strip()+"----- please create SKU ID of product"))
                    order_create = self.env['sale.order'].create(order_vals)
                    already_so_id = order_create
                    print("------------------order_create-------------", order_create)
                    count = count+1
                    print("-----------------count----------------------", count)
                else:
                    sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['SKU']].strip())])
                    if sk_id:
                        order_write = already_so_id.write({'order_line': [(0,0,{'product_id': sk_id.product_id.id, 'name': sk_id.product_id.name, 'sku_id': sk_id.id, 'sku_name': sk_id.name, 'name': sk_id.product_id.name, 'product_uom_qty': row[headers['Quantity']].strip(), 'price_unit': row[headers['Cost']].strip()})]})
                        print("-----------------order_write--------------", order_write)
                        count = count+1
                        print("++++++++++++++++++count++++++++++++++++++", count)
                    else:
                        raise Warning(_("The Product -----"+row[headers['Title']].strip()+"----- has not been map with ---------"+row[headers['SKU']].strip()+"----- please create SKU ID of product"))