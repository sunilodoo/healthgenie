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
    # order_b2b_b2c = fields.Selection([('b2b', 'B2B'), ('b2c', 'B2C')], string="Order(B2B/B2C)", default=False, required=True)
    order_file = fields.Binary(string='Order CSV File', required=True, help='File should be separated by comma (,) and quoted using Quote character (")')

    def action_confirm_so(self):
        print("-----------action_confirm_so---------", self)
        action_confirm_so_draft=self.env['sale.order'].search([('state', '=', 'draft')], order='id asc')
        # action_confirm_so_draft=self.env['sale.order'].search([('state', '=', 'draft')], order='id asc')
        print("-----------action_confirm_so_draft------", action_confirm_so_draft)
        for soaf in action_confirm_so_draft:
            if soaf.warehouse_id.code != 'WH':
                print("-----------------soaf$$$so--------------------", soaf.name)
                print("-----------------soaf--------------------", soaf.action_confirm())
            # break;
    def action_create_invoice_so(self):
        print("-----------action_create_invoice_so---------", self)
        so_to_inv_ids = self.env['sale.order'].search([('invoice_status', '=', 'to invoice')], order='id asc')
        print("-----------so_to_inv_ids------", so_to_inv_ids)
        for soci in so_to_inv_ids:
            print("-----------------soci--------------------", soci.name)
            print("-----------------soci--------------------", soci._create_invoices())
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

    def states_sku_check(self):
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
        # states_ids = self.env['res.country.state'].search([('country_id', '=', 104)])
        # state_names = [i.name for i in states_ids]
        # state_code = [j.code for j in states_ids]
        sku_ids = self.env['sku.mapping'].search([])
        sku_names = [j.name for j in sku_ids]
        # print("------------state_name------", state_names)
        for row in reader:
            count = count+1
            if row[headers['order-status']].strip() != 'Cancelled':
                if row[headers['sales-channel']].strip() != 'Non-Amazon':
                    if row[headers['item-status']].strip() != 'Cancelled':
                        # state_name = row[headers['ship-state']].strip()
                        ship_postal_code = row[headers['ship-postal-code']].strip()
                        if not self.env['pincode.state'].search([('name', '=', ship_postal_code)]):
                            self.env['sale.order.missing'].create({'channel_name': row[headers['sales-channel']], 'order_no': row[headers['amazon-order-id']].strip(), 'pincode': row[headers['ship-postal-code']]})
                            # raise UserError(_("The ship-postal-code "+ship_postal_code+' is not found. '+' in line '+str(count)+ '--as '+row[headers['amazon-order-id']]))
                            # print("--------------count-----------", count)
                        # if state_name not in state_names:
                        #     if state_name.upper() not in state_code:
                        #         raise UserError(_("The State-shipping "+state_name+' is not found. '+' in line '+str(count)+ '--as '+row[headers['amazon-order-id']]))
                        #         print("--------------count-----------", count)
                        if row[headers['sku']].strip() not in sku_names:
                            self.env['sale.order.missing'].create({'channel_name': row[headers['sales-channel']], 'order_no': row[headers['amazon-order-id']].strip(), 'sku_name': row[headers['sku']]})
                            # raise Warning(_("The SKU_ID "+row[headers['sku']].strip()+' is not found. '+' in line '+str(count)+ '--as '+row[headers['amazon-order-id']].strip()))
                        t_p = self.env['res.partner'].search([('name', '=', row[headers['fulfillment-channel']].strip())])
                        if not t_p:
                            raise Warning(_("The Third Party "+row[headers['fulfillment-channel']].strip()+' is not found. Please Create in Contects'))

    def warehouse_check_gst_mtr_b2b(self):
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
        warehouse_ids = self.env['stock.warehouse'].search([])
        warehouse_code = [k.code for k in warehouse_ids]
        print("------------warehouse_names------", warehouse_code)
        for row in reader:
            count = count+1
            wh_code = row[headers['Warehouse Id']].strip()
            if not wh_code:
                raise Warning(_("The Warehouse "+' is not '+' in line '+str(count)+ '--as '+row[headers['Order Id']].strip()))
            if wh_code not in warehouse_code:
                raise Warning(_("The Warehouse "+row[headers['Warehouse Id']].strip()+' is not found. '+' in line '+str(count)+ '--as '+row[headers['Order Id']].strip()))

    def warehouse_check_gst_mtr_b2c(self):
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
        warehouse_ids = self.env['stock.warehouse'].search([])
        warehouse_code = [k.code for k in warehouse_ids]
        print("------------warehouse_names------", warehouse_code)
        for row in reader:
            count = count+1
            wh_code = row[headers['Warehouse Id']].strip()
            if not wh_code:
                raise Warning(_("The Warehouse "+' is not '+' in line '+str(count)+ '--as '+row[headers['Order Id']].strip()))
            if wh_code not in warehouse_code:
                raise Warning(_("The Warehouse "+row[headers['Warehouse Id']].strip()+' is not found. '+' in line '+str(count)+ '--as '+row[headers['Order Id']].strip()))
    def warehouse_check_shipment(self):
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
        warehouse_ids = self.env['stock.warehouse'].search([])
        warehouse_code = [k.code for k in warehouse_ids]
        print("------------warehouse_names------", warehouse_code)
        for row in reader:
            count = count+1
            wh_code = row[headers['FC']].strip()
            if not wh_code:
                raise Warning(_("The Warehouse "+' is not '+' in line '+str(count)+ '--as '+row[headers['Amazon Order Id']].strip()))
            if wh_code not in warehouse_code:
                raise Warning(_("The Warehouse "+row[headers['FC']].strip()+' is not found. '+' in line '+str(count)+ '--as '+row[headers['Amazon Order Id']].strip()))

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
        print("------------headers------", headers)
        count =1
        already_order_id = ''
        already_so_id = ''
        already_amazon_order_id = ''
        for row in reader:
            # print("------------------------------------------------------------------------------------------------------------")
            current_order_id = row[headers['amazon-order-id']].strip()
            amazon_order_id = self.env['sale.order'].search([('order_id', '=', current_order_id)])
            # print("-----------amazon_order_id-------", amazon_order_id)
            # row[headers['order-status']].strip() == 'Cancelled'
            # row[headers['sales-channel']].strip() != 'Non-Amazon'
            # row[headers['item-status']].strip() != 'Cancelled'
            # row[headers['item-status']].strip() != 'Unshipped'
            if row[headers['order-status']].strip() != 'Cancelled':
                if row[headers['sales-channel']].strip() != 'Non-Amazon':
                    if row[headers['item-status']].strip() != 'Cancelled':
                        if not amazon_order_id or already_amazon_order_id == current_order_id:
                            # print("-----------amazon_order_id-------", amazon_order_id)
                            order_id = current_order_id
                            # print("-----------order_id-------", order_id)
                            # print("-----------already_amazon_order_id-------", already_amazon_order_id)
                            if current_order_id != already_amazon_order_id:
                                already_amazon_order_id = current_order_id
                                s_p_c = row[headers['ship-postal-code']].strip()
                                customer_vals ={
                                    'name': 'Sinew Customer',
                                    # 'name': current_order_id+'-Sinew',
                                    # 'street': 'B-13/2, Okhla Phase-2',
                                    'city': row[headers['ship-city']].strip(),
                                    'zip': s_p_c,
                                }
                                s_p_c_id = self.env['pincode.state'].search([('name', '=', s_p_c)])
                                if s_p_c_id:
                                    customer_vals['state_id'] =  s_p_c_id.state_id.id
                                    customer_vals['country_id'] =  s_p_c_id.country_id.id
                                else:
                                    raise Warning(_("The State Pincode"+s_p_c+' is not found. Please Create Pincode in Pincode With State'))
                                # state_ids = self.env['res.country.state'].search([('name', '=', row[headers['ship-state']].strip()), ('country_id', '=', 104)])
                                # if state_ids:
                                #     customer_vals['state_id'] =  state_ids[0].id
                                #     customer_vals['country_id'] =  104
                                # else:
                                #     raise Warning(_("The State "+row[headers['ship-state']].strip()+' is not found. Please Create state in Fed. state'))
                                customer_id = self.env['res.partner'].create(customer_vals)
                                d_o = datetime.strptime(row[headers['purchase-date']].strip(), "%Y-%m-%dT%H:%M:%S%z")
                                # inv_d = datetime.strptime(row[headers['purchase-date']].strip(), "%Y-%m-%dT%H:%M:%S%z").date()
                                # inv_d = datetime.strptime(row[headers['last-updated-date']].strip(), "%Y-%m-%dT%H:%M:%S%z").date()
                                order_vals = {
                                    'partner_id': customer_id.id,
                                    'order_id': order_id,
                                    'date_order': d_o.utcnow(),
                                    'order_date': d_o.date(),
                                    'order_type': row[headers['fulfillment-channel']].strip(),
                                    'order_category':'b2c',
                                    # 'order_category': 'b2b' if row[headers['is-business-order']].strip().upper() == 'TRUE' else 'b2c',
                                    'invoice_no': current_order_id,
                                    'invoice_date': d_o.date(),
                                    # 'invoice_date': inv_d,
                                    # 'tracking_no': row[headers['tracking id']].strip(),
                                    # 'delivery_partner_name': row[headers['Delivery partner']].strip()
                                }
                                t_p = self.env['res.partner'].search([('name', '=', row[headers['fulfillment-channel']].strip())])
                                if t_p:
                                    order_vals['third_party'] =  t_p[0].id
                                else:
                                    raise Warning(_("The Third Party "+row[headers['fulfillment-channel']].strip()+' is not found. Please Create in Contects'))
                                sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['sku']].strip())])
                                quantity = int(row[headers['quantity']].strip()) if row[headers['quantity']].strip() else 0
                                if sk_id:
                                    # print("--------------quantity------", type(quantity))
                                    item_price = float(row[headers['item-price']].strip()) if row[headers['item-price']].strip() else 0.0
                                    portal_price = item_price/quantity if quantity>=1 else 0.0
                                    s_p = float(row[headers['shipping-price']].strip()) if row[headers['shipping-price']].strip() else 0.0
                                    s_p_d = float(row[headers['ship-promotion-discount']].strip()) if row[headers['ship-promotion-discount']].strip() else 0.0 
                                    line_vals ={
                                        'product_id': sk_id[0].product_id.id,
                                        'name': sk_id[0].product_id.name,
                                        'sku_id': sk_id[0].id,
                                        'sku_name': sk_id[0].default_code,
                                        # 'product_uom_qty': row[headers['quantity']].strip(),
                                        'product_uom_qty': quantity,
                                        # row[headers['quantity']].strip()
                                        'portal_price': portal_price,
                                        'unit_shipping_charges': s_p-s_p_d
                                    }
                                    order_vals['order_line'] = [(0,0, line_vals)]
                                else:
                                    raise Warning(_("The Product -----"+row[headers['product-name']].strip()+"----- has not been map with ---------"+row[headers['sku']].strip()+"----- please create SKU ID of product"))
                                original_order = row[headers['original-order-id']].strip()
                                if row[headers['is-replacement-order']].strip().upper() != 'TRUE':
                                    # print("---------------asd--------", row[headers['is-replacement-order']].strip().upper())
                                    order_create = self.env['sale.order'].create(order_vals)
                                    if order_create and row[headers['order-status']].strip() == 'Cancelled':
                                        order_create.action_cancel()
                                    # print("-------order_create-", order_create)
                                    already_so_id = order_create
                                    # print("-------already_so_id-", already_so_id)
                                    print("------------------order_create-------------", order_create)
                                elif (row[headers['is-replacement-order']].strip().upper() == 'TRUE') and original_order:
                                    # print("-----------------------'is-replacement-order---------", row[headers['is-replacement-order']].strip().upper())
                                    original_order_id = self.env['sale.order'].search([('order_id', '=', original_order)])
                                    # print("--------------original_order_id------", original_order_id)
                                    portal_price = 0.0
                                    product_uom_qty = 0.0
                                    unit_shipping_charges = 0.0
                                    # print("------------0--portal_price------", portal_price)
                                    if original_order_id:
                                        for i in original_order_id.order_line:
                                            if i.sku_id.name == row[headers['sku']].strip():
                                                product_uom_qty = i.product_uom_qty
                                                portal_price = i.portal_price
                                                unit_shipping_charges = i.unit_shipping_charges
                                        order_vals['order_line'][0][2]['product_uom_qty'] = product_uom_qty
                                        order_vals['order_line'][0][2]['portal_price'] = portal_price
                                        order_vals['order_line'][0][2]['unit_shipping_charges'] = unit_shipping_charges
                                        order_vals['original_order_id'] = row[headers['original-order-id']].strip()
                                        order_vals['is_replacement'] = True
                                    # print("-----------------------order_vals---------", order_vals)
                                    order_create = self.env['sale.order'].create(order_vals)
                                    if order_create and row[headers['order-status']].strip() == 'Cancelled':
                                    # if order_create and quantity == 0:
                                        order_create.action_cancel()
                                    already_so_id = order_create
                                    print("-----------------------order_create---------", order_create)
                                    # print("-----------------------already_so_id---------", already_so_id)
                                else:
                                    raise Warning(_("The original order id  -----"+row[headers['original-order-id']].strip()+"----- is not created already please create first ---------"))
                                # if row[headers['order-status']].strip() == 'Cancelled' or quantity == 0:
                                #         print("-----------------------Cancelled---------")
                                #         act_can = amazon_order_id.action_cancel()
                                #         print("-----------------act_can------Cancelled---------", act_can)
                                # elif row[headers['order-status']].strip() == 'Pending':
                                #     print("-----------------------Pending---------")
                                # elif row[headers['order-status']].strip() == 'Shipped':
                                #     if amazon_order_id.state == 'draft':
                                #         act_conf = amazon_order_id.action_confirm()
                                #         print("---------------act_conf---------Shipped--------", act_conf)
                                #         cret_inv = amazon_order_id.env['sale.advance.payment.inv'].create_invoices()
                                #         print("------------------------cret_inv--------", cret_inv)
                                #     print("------------------------Shipped--------")
                                # elif row[headers['order-status']].strip() == 'Shipped - Delivered to Buyer':
                                #     print("-----------------------Shipped - Delivered to Buyer---------")
                                # elif row[headers['order-status']].strip() == 'Shipped - Picked Up':
                                #     print("----------------------Shipped - Picked Up----------")
                                # elif row[headers['order-status']].strip() == 'Shipped - Returned to Seller':
                                #     print("---------------------Shipped - Returned to Seller-----------")
                                # elif row[headers['order-status']].strip() == 'Shipped - Returning to Seller':
                                #     print("--------------------Shipped - Returning to Seller------------")
                                count = count+1
                                print("---------------------------count---------------------", count)
                            else:
                                sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['sku']].strip())])
                                if sk_id:
                                    quantity = int(row[headers['quantity']].strip()) if row[headers['quantity']].strip() else 0
                                    if quantity > 0:
                                        if row[headers['is-replacement-order']].strip().upper() != 'TRUE':
                                            item_price = float(row[headers['item-price']].strip()) if row[headers['item-price']].strip() else 0.0
                                            portal_price = item_price/quantity if quantity>=1 else 0.0
                                            s_p = float(row[headers['shipping-price']].strip()) if row[headers['shipping-price']].strip() else 0.0
                                            s_p_d = float(row[headers['ship-promotion-discount']].strip()) if row[headers['ship-promotion-discount']].strip() else 0.0 
                                            write_vals={
                                                'product_id': sk_id.product_id.id,
                                                'name': sk_id.product_id.name,
                                                'sku_id': sk_id.id,
                                                'sku_name': sk_id.name,
                                                'name': sk_id.product_id.name,
                                                'product_uom_qty': quantity,
                                                'portal_price': portal_price,
                                                'unit_shipping_charges': s_p-s_p_d
                                            }
                                            order_write = already_so_id.write({'order_line': [(0,0, write_vals)]})
                                        elif row[headers['is-replacement-order']].strip().upper() == 'TRUE':
                                            original_order = row[headers['original-order-id']].strip()
                                            if original_order:
                                                original_order_id = self.env['sale.order'].search([('order_id', '=', original_order)])
                                                portal_price = 0.0
                                                product_uom_qty = 0.0
                                                unit_shipping_charges = 0.0
                                                # print("------------0--portal_price------", portal_price)
                                                if original_order_id:
                                                    for i in original_order_id.order_line:
                                                        if i.sku_id.name == row[headers['sku']].strip():
                                                            product_uom_qty = i.product_uom_qty
                                                            portal_price = i.portal_price
                                                            unit_shipping_charges = i.unit_shipping_charges
                                                write_vals={
                                                    'product_id': sk_id.product_id.id,
                                                    'name': sk_id.product_id.name,
                                                    'sku_id': sk_id.id,
                                                    'sku_name': sk_id.name,
                                                    'name': sk_id.product_id.name,
                                                    'product_uom_qty': product_uom_qty,
                                                    'portal_price': portal_price,
                                                    'unit_shipping_charges': unit_shipping_charges
                                                }
                                                order_write = already_so_id.write({'order_line': [(0,0, write_vals)]})
                                                print("-----------------order_write--------------", order_write)
                                            else:
                                                raise Warning(_("The original_order_id --2---"+row[headers['original-order-id']]+"----of----amazon_order_id-----"+row[headers['current_order_id']].strip()+"-----is not created before"))
                                else:
                                    raise Warning(_("The Product -----"+row[headers['product-name']]+"----- has not been map with ---------"+row[headers['sku']].strip()+"----- please create SKU ID of product"))
                                print("-----------------else-------count----------", count)
                                count+=1
                        else:
                            if row[headers['order-status']].strip() == 'Cancelled':
                                # quantity = int(row[headers['quantity']].strip()) if row[headers['quantity']] else 0
                                if amazon_order_id.state != 'cancel' and amazon_order_id.state == 'draft':
                                    # if quantity == 0:
                                    print("-------------else----------Cancelled---------")
                                    act_can = amazon_order_id.action_cancel()
                                    print("----------else-------act_can------Cancelled---------", act_can)
                                    # if quantity >= 1:
                                    #     print("-------------else----------Cancelled---------")
                                    #     act_can = amazon_order_id.action_confirm()
                                    #     # act_can = amazon_order_id.action_confirm()  #For RTO
                                    #     print("----------else-------act_can------Cancelled---------", act_can)
                            # elif row[headers['order-status']].strip() == 'Pending':
                            #     print("--------------else---------Pending---------")
                            # elif row[headers['order-status']].strip() == 'Shipped':
                            #     print("--------------else----------Shipped--------")
                            #     if amazon_order_id.state == 'draft':
                            #         act_conf = amazon_order_id.action_confirm()
                            #         print("-------else-------act_conf---------Shipped--------", act_conf)
                            #         cret_inv = amazon_order_id.env['sale.advance.payment.inv'].create_invoices()
                            #         print("------------else------------cret_inv--------", cret_inv)
                            # elif row[headers['order-status']].strip() == 'Shipped - Delivered to Buyer':
                            #     print("------------else-----------Shipped - Delivered to Buyer---------")
                            # elif row[headers['order-status']].strip() == 'Shipped - Picked Up':
                            #     print("--------------else--------Shipped - Picked Up----------")
                            # elif row[headers['order-status']].strip() == 'Shipped - Returned to Seller':
                            #     print("--------------else-------Shipped - Returned to Seller-----------")
                            # elif row[headers['order-status']].strip() == 'Shipped - Returning to Seller':
                            #     print("--------------else------Shipped - Returning to Seller------------")
                            count+=1
                        print("-----------count-----", count)

    def gst_mtr_b2b_warehouse_update(self):
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
        for row in reader:
            order_id = self.env['sale.order'].search([('order_id', '=', row[headers['Order Id']].strip())])
            # print("-----------order_id-------", order_id)
            wh_code = row[headers['Warehouse Id']].strip()
            if order_id and order_id.state == 'draft':
                wh_id = self.env['stock.warehouse'].search([('code', '=', wh_code)])
                # print("-----------------wh_id----", wh_id)
                if wh_code and wh_id:
                    wh_update = order_id.write({'warehouse_id': wh_id[0].id})
                    # print("------------wh_id-------", wh_id.name)
                    # print("------------wh_update-------", wh_update)
                # else:
                #     raise Warning(_("The Warehouse "+wh_code+' is not found. Please Create in Inventory as Warehouse'))
                if not order_id.partner_id.vat:
                    gstn_no = row[headers['Customer Bill To Gstid']].strip()
                    if gstn_no:
                        order_id.partner_id.write({'vat': gstn_no})
                        order_id.write({'order_category': 'b2b'})
                partner_name = row[headers['Buyer Name']].strip()
                if partner_name:
                    order_id.partner_id.write({'name': partner_name})
            count+=1
            print("-----------------count----------", count)

    def gst_mtr_b2c_warehouse_update(self):
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
        for row in reader:
            order_id = self.env['sale.order'].search([('order_id', '=', row[headers['Order Id']].strip())])
            # print("-----------order_id-------", order_id)
            wh_code = row[headers['Warehouse Id']].strip()
            if order_id and order_id.state == 'draft':
                wh_id = self.env['stock.warehouse'].search([('code', '=', wh_code)])
                # print("-----------------wh_id----", wh_id)
                if wh_code and wh_id:
                    wh_update = order_id.write({'warehouse_id': wh_id[0].id})
                    # print("------------wh_id-------", wh_id.name)
                    # print("------------wh_update-------", wh_update)
                # else:
                #     raise Warning(_("The Warehouse "+wh_code+' is not found. Please Create in Inventory as Warehouse'))
            count+=1
            print("-----------------count----------", count)

    def shipment_warehouse_update(self):
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
        # print("------------headers------", headers)
        count =1
        for row in reader:
            print("----------o---------", row[headers['FC']].strip())
            a_o_i = row[headers['Amazon Order Id']].strip()
            # print("----------a_o_i--------", a_o_i)
            order_id = self.env['sale.order'].search([('order_id', '=', a_o_i)])
            # print("-----------order_id-------", order_id)
            wh_code = row[headers['FC']].strip()
            if order_id and order_id.state == 'draft':
                wh_id = self.env['stock.warehouse'].search([('code', '=', row[headers['FC']].strip())])
                if wh_code and wh_id:
                    wh_update = order_id.write({'warehouse_id': wh_id[0].id})
                    # print("------------wh_id-------", wh_id.code)
                    # print("------------wh_update-------", wh_update)
                # else:
                #     raise Warning(_("The Warehouse "+wh_code+' is not found. Please Create in Inventory as Warehouse'))
            count+=1
            print("-----------------count----------", count)


    def Not_do_import(self):
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
                        'order_type': row[headers['fulfillment-channel']].strip(),
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
                        order_vals['order_line'] = [(0,0,{'product_id': sk_id[0].product_id.id, 'name': sk_id[0].product_id.name, 'sku_id': sk_id[0].id, 'sku_name': sk_id[0].default_code, 'product_uom_qty': row[headers['quantity']].strip(), 'portal_price': float( row[headers['item-unit-price']].strip()), 'unit_shipping_charges': row[headers['unit-shipping-charges']].strip()})]
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
                        order_write = already_so_id.write({'order_line': [(0,0,{'product_id': sk_id.product_id.id, 'name': sk_id.product_id.name, 'sku_id': sk_id.id, 'sku_name': sk_id.name, 'name': sk_id.product_id.name, 'product_uom_qty': row[headers['quantity']].strip(), 'portal_price': float( row[headers['item-unit-price']].strip()), 'unit_shipping_charges': row[headers['unit-shipping-charges']].strip()})]})
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