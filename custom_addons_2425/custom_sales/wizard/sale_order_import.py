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

    # def update_M_O_S(self):
    #     f = base64.b64decode(self.order_file)
    #     data_file = io.StringIO(f.decode("utf-8"))
    #     reader = csv.reader(data_file, delimiter=',')
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     count =1
    #     for row in reader:
    #         count = count+1
    #         p_order_id = row[headers['amazon-order-id']].strip()
    #         amazon_order_id = self.env['account.move'].search([('order_id', '=', p_order_id), ('state', '=', 'posted')])
    #         if amazon_order_id and amazon_order_id[0]:
    #             amazon_order_id.update({'month_of_sale': self.month_of_sale})
    #             amazon_order_id.so_id.update({'month_of_sale': self.month_of_sale})

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
    # def action_create_invoice_so(self):
    #     print("-----------action_create_invoice_so---------", self)
    #     so_to_inv_ids = self.env['sale.order'].search([('invoice_status', '=', 'to invoice')], order='id asc')
    #     print("-----------so_to_inv_ids------", so_to_inv_ids)
    #     for soci in so_to_inv_ids:
    #         print("-----------------soci--------------------", soci.name)
    #         print("-----------------soci--------------------", soci._create_invoices())
    #         break;
    # def states_sku_check(self):
    #     f = base64.b64decode(self.order_file)
    #     data_file = io.StringIO(f.decode("utf-8"))
    #     reader = csv.reader(data_file, delimiter=',')
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     count =1
    #     # states_ids = self.env['res.country.state'].search([('country_id', '=', 104)])
    #     # state_names = [i.name for i in states_ids]
    #     # state_code = [j.code for j in states_ids]
    #     sku_ids = self.env['sku.mapping'].search([])
    #     sku_names = [j.name for j in sku_ids]
    #     # print("------------state_name------", state_names)
    #     for row in reader:
    #         count = count+1
    #         if row[headers['order-status']].strip() != 'Cancelled':
    #             if row[headers['sales-channel']].strip() != 'Non-Amazon':
    #                 if row[headers['item-status']].strip() != 'Cancelled':
    #                     # state_name = row[headers['ship-state']].strip()
    #                     ship_postal_code = row[headers['ship-postal-code']].strip()
    #                     if not self.env['pincode.state'].search([('name', '=', ship_postal_code)]):
    #                         self.env['sale.order.missing'].create({'channel_name': row[headers['sales-channel']], 'order_no': row[headers['amazon-order-id']].strip(), 'pincode': row[headers['ship-postal-code']]})
    #                         # raise UserError(_("The ship-postal-code "+ship_postal_code+' is not found. '+' in line '+str(count)+ '--as '+row[headers['amazon-order-id']]))
    #                         # print("--------------count-----------", count)
    #                     # if state_name not in state_names:
    #                     #     if state_name.upper() not in state_code:
    #                     #         raise UserError(_("The State-shipping "+state_name+' is not found. '+' in line '+str(count)+ '--as '+row[headers['amazon-order-id']]))
    #                     #         print("--------------count-----------", count)
    #                     if row[headers['sku']].strip() not in sku_names:
    #                         self.env['sale.order.missing'].create({'channel_name': row[headers['sales-channel']], 'order_no': row[headers['amazon-order-id']].strip(), 'sku_name': row[headers['sku']]})
    #                         # raise Warning(_("The SKU_ID "+row[headers['sku']].strip()+' is not found. '+' in line '+str(count)+ '--as '+row[headers['amazon-order-id']].strip()))
    #                     t_p = self.env['res.partner'].search([('name', '=', row[headers['fulfillment-channel']].strip())])
    #                     if not t_p:
    #                         raise Warning(_("The Third Party "+row[headers['fulfillment-channel']].strip()+' is not found. Please Create in Contects'))
    #                     w_i = self.env['stock.warehouse'].search([('code', '=', row[headers['warehouse_code']].strip())])
    #                     if w_i:
    #                         pass
    #                     else:
    #                         raise Warning(_("The Warehouse Code"+row[headers['warehouse_code']].strip()+' is not found. Please Create in Inventory as Warehouse'))

    # def warehouse_check_gst_mtr_b2b(self):
    #     f = base64.b64decode(self.order_file)
    #     data_file = io.StringIO(f.decode("utf-8"))
    #     reader = csv.reader(data_file, delimiter=',')
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     count =1
    #     warehouse_ids = self.env['stock.warehouse'].search([])
    #     warehouse_code = [k.code for k in warehouse_ids]
    #     print("------------warehouse_names------", warehouse_code)
    #     for row in reader:
    #         count = count+1
    #         wh_code = row[headers['Warehouse Id']].strip()
    #         if not wh_code:
    #             raise Warning(_("The Warehouse "+' is not '+' in line '+str(count)+ '--as '+row[headers['Order Id']].strip()))
    #         if wh_code not in warehouse_code:
    #             raise Warning(_("The Warehouse "+row[headers['Warehouse Id']].strip()+' is not found. '+' in line '+str(count)+ '--as '+row[headers['Order Id']].strip()))

    # def warehouse_check_gst_mtr_b2c(self):
    #     f = base64.b64decode(self.order_file)
    #     data_file = io.StringIO(f.decode("utf-8"))
    #     reader = csv.reader(data_file, delimiter=',')
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     count =1
    #     warehouse_ids = self.env['stock.warehouse'].search([])
    #     warehouse_code = [k.code for k in warehouse_ids]
    #     print("------------warehouse_names------", warehouse_code)
    #     for row in reader:
    #         count = count+1
    #         wh_code = row[headers['Warehouse Id']].strip()
    #         if not wh_code:
    #             raise Warning(_("The Warehouse "+' is not '+' in line '+str(count)+ '--as '+row[headers['Order Id']].strip()))
    #         if wh_code not in warehouse_code:
    #             raise Warning(_("The Warehouse "+row[headers['Warehouse Id']].strip()+' is not found. '+' in line '+str(count)+ '--as '+row[headers['Order Id']].strip()))
    # def warehouse_check_shipment(self):
    #     f = base64.b64decode(self.order_file)
    #     data_file = io.StringIO(f.decode("utf-8"))
    #     reader = csv.reader(data_file, delimiter=',')
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     count =1
    #     warehouse_ids = self.env['stock.warehouse'].search([])
    #     warehouse_code = [k.code for k in warehouse_ids]
    #     print("------------warehouse_names------", warehouse_code)
    #     for row in reader:
    #         count = count+1
    #         wh_code = row[headers['FC']].strip()
    #         if not wh_code:
    #             raise Warning(_("The Warehouse "+' is not '+' in line '+str(count)+ '--as '+row[headers['Amazon Order Id']].strip()))
    #         if wh_code not in warehouse_code:
    #             raise Warning(_("The Warehouse "+row[headers['FC']].strip()+' is not found. '+' in line '+str(count)+ '--as '+row[headers['Amazon Order Id']].strip()))



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
        # print("------------headers------", headers)
        list_reader = list(reader)
        l_reader = len(list_reader)
        # print("-------------------#--------", list_reader)
        # print("-------------------#--------", l_reader)
        if list_reader[1][1] > list_reader[l_reader-1][1]:
            # print("------------1----", list_reader[1][1])
            # print("------------2----", list_reader[l_reader-1][1])
            raise UserError(_('Order Date must be in increasing order.'))
        #----------------------------------------------------one-time-check----------------------------------------------------
        # count =1
        # for row in reader:
        #     count+=1
        #     if not purchase_date:
        #         purchase_date = row[headers['purchase-date']].strip()
        #     if purchase_date and purchase_date > row[headers['purchase-date']].strip():
        #         raise Warning(_("purchase-date must be in increasing order."))
        #     t_p_a = self.env['res.partner'].search([('name', '=', 'Amazon')])
        #     t_p_m = self.env['res.partner'].search([('name', '=', 'Merchant')])
        #     if not t_p_a:
        #         raise Warning(_("fulfillment-channel as 'Amazon' must be in Contects "))
        #     if not t_p_m:
        #         raise Warning(_("fulfillment-channel as 'Merchant' must be in Contects "))
        #     if count >= 4:
        #         break
        #     print("------------break------")
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
        # print("------------------count--------------", count)
        print("------------headers------", headers)
        warehouse_ids = self.env['stock.warehouse'].search([])
        warehouse_code = [k.code for k in warehouse_ids]
        for row in reader:
            print("--------------------------------2----------------")
            # if row[headers['order-status']].strip() != 'Cancelled' and row[headers['sales-channel']].strip() != 'Non-Amazon' and row[headers['item-status']].strip() != 'Cancelled':
            portal_o_id = row[headers['Order ID']].strip()
            odoo_o_id = self.env['sale.order'].search([('order_id', '=', portal_o_id)])
            print("odoo_o_id....................",odoo_o_id)
            if odoo_o_id:
                raise UserError(_("Order ID "+portal_o_id+' in line '+str(count)+' is already exists'))
            portal_name = row[headers['Portal Name']].strip()
            portal_name_id = self.env['res.portal'].search([('name', '=', portal_name)])
            if not portal_name_id:
                raise UserError(_("Portal Name "+portal_name+' in line '+str(count)+' is not found'))
            o_d = row[headers['Order Date']].strip()
            order_date = datetime.strptime(o_d, "%d/%m/%Y")
            i_d = row[headers['Invoice Date']].strip()
            invoice_date = datetime.strptime(i_d, "%d/%m/%Y")
            #----------------------------------produt----------------------------
            if portal_name_id.name == 'Flipkart':
                sk = row[headers['sku']].strip()
                sk_id = self.env['sku.mapping'].search([('name', '=', sk)])
                print("sk_id::::::::::::::::::::", sk_id)
                if not sk_id:
                    raise UserError(_("sku "+sk+' in line '+str(count)+'--in k-id '+portal_o_id+' is not found. create in SKU Mapping'))
                fsn = row[headers['FSN']].strip()
                fsn_id = self.env['sku.mapping'].search([('id_number', '=', fsn)])
                if not fsn_id:
                    raise UserError(_("fsn "+fsn+' in line '+str(count)+' is not found. update in SKU Mapping'))

            # mag = row[headers['Product Magento ID']].strip()
            # magento_id = self.env['product.product'].search([('default_code', '=', mag)])
            # if not magento_id:
            #     raise UserError(_("Product Magento ID "+mag+' in line '+str(count)+'--in Order ID '+portal_o_id+' is not found. create in Product'))
            #----------------------------------produt----------------------------
            s_p_c = row[headers['Customer Pincode']].strip()
            s_p_c_id = self.env['pincode.state'].search([('name', '=', s_p_c)])
            if not s_p_c_id:
                raise UserError(_("Customer Pincode "+s_p_c+' is not found in line. '+str(count)+' Please Create Pincode in Pincode With State'))
            qty = int(row[headers['Quantity']].strip())
            portal_price = float(row[headers['Invoice Value Excluding Shipping charges']].strip())
            shipping_charges = float(row[headers['Shipping Charges']].strip())
            portal_price = float(row[headers['Invoice Value Including Shipping charges']].strip())
            # i_r_o = row[headers['is-replacement-order']].strip().upper()
            # if i_r_o == 'TRUE' or i_r_o == 'FALSE':
            #     pass
            # else:
            #     raise UserError(_("is-replacement-order must be TRUE or FALSE in line"+str(count)+'--in order-id '+a_o_i))
            # if i_r_o == 'TRUE':
            #     if not row[headers['original-order-id']].strip():
            #         raise UserError(_("original-order-id  order is must in line "+str(count)+'--in order-id '+a_o_i))
            # i_b_o = row[headers['is-business-order']].strip().upper()
            # if i_b_o == 'TRUE' or i_b_o == 'FALSE':
            #     pass
            # else:
            #     raise UserError(_("is-business-order must be TRUE or FALSE in line"+str(count)+'--in order-id '+a_o_i))
            # if i_b_o == 'TRUE':
            #     if not row[headers['gstin']].strip():
            #         raise UserError(_("gstin number of business order is must in line "+str(count)+'--in order-id '+a_o_i))
            #     if len(row[headers['gstin']].strip()) != 15:
            #         print("------------gstin------", row[headers['gstin']].strip())
            #         print("------------llgstin------", len(row[headers['gstin']].strip()))
            #         raise UserError(_("gstin number of business order is must be valid of 15 digits in line "+str(count)+'--in order-id '+a_o_i))
            fc = row[headers['Wharehouse']].strip()
            if fc not in warehouse_code:
                raise Warning(_("Wharehouse "+fc+' is not found. '+' in line '+str(count)+'--in Order ID '+portal_o_id))
            print("------------------count--------------", count)
            # print("------------------amz_order--------------", row[headers['amazon-order-id']].strip())
            count+=1
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
        print("------------headers------", headers)
        count =2
        for row in reader:
            # if row[headers['order-status']].strip() != 'Cancelled' and row[headers['sales-channel']].strip() != 'Non-Amazon' and row[headers['item-status']].strip() != 'Cancelled':
            current_order_id = row[headers['Order ID']].strip()
            order_id = self.env['sale.order'].search([('order_id', '=', current_order_id)])
            # if order_id:
            #     if order_id.state == 'draft':
            #         pass
            #     else:
            #         raise UserError(_("amazon_order_id "+str(current_order_id)+' is already exists with confirmed'))
            # if not amazon_order_id or already_amazon_order_id == current_order_id:
            #-------------------------------------------product_line------------------------------------------------------------------------------------------------------------------
            # sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['sku']].strip())])
            pro_pro_id = self.env['product.product'].search([('default_code', '=', row[headers['sku']].strip())])
            sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['sku']].strip())])
            line_vals={
                'product_uom_qty': int(row[headers['Quantity']].strip()) if row[headers['Quantity']].strip() else 0,
                'portal_price': float(row[headers['Invoice Value Excluding Shipping charges']].strip()) if row[headers['Invoice Value Excluding Shipping charges']].strip() else 0.0,
                'shipping_charges': float(row[headers['Shipping Charges']].strip()) if row[headers['Shipping Charges']].strip() else 0.0,
                # 'portal_price' = float(row[headers['Invoice Value Including Shipping charges']].strip()) if row[headers['Invoice Value Including Shipping charges']].strip() else 0.0
            }

            # if sk_id:
            #     item_price = float(row[headers['item-price']].strip()) if row[headers['item-price']].strip() else 0.0
            #     portal_price = item_price/quantity if quantity>=1 else 0.0
            #     line_vals['product_id'] = sk_id[0].product_id.id
            #     line_vals['name'] = sk_id[0].product_id.name
            #     line_vals['sku_id'] = sk_id[0].id
            #     line_vals['sku_name'] = sk_id[0].default_code
            #     line_vals['portal_price'] = portal_price
            if sk_id:
                print("-------------111111111111111-----------------------")
                line_vals['product_id'] = sk_id[0].product_id.id
                line_vals['name'] = sk_id[0].product_id.name
                line_vals['product_default_code'] = sk_id.default_code
                line_vals['sku_id'] = sk_id[0].id
                line_vals['sku_name'] = sk_id[0].default_code
            else:
                print("-------------2222222222222222222-----------------------")
                line_vals['product_id'] = pro_pro_id.id
                line_vals['name'] = pro_pro_id.name
                line_vals['product_default_code'] = pro_pro_id.default_code
                # line_vals['sku_id'] = pro_pro_id[0].id
                # line_vals['sku_name'] = pro_pro_id[0].default_code
            #------------------------------------------------------order-------------------------------------------------------------------------------------------------------
            if not order_id:
                customer_vals ={
                    'name': row[headers['Customer Name']].strip(),
                    'street': row[headers['Customer Address']].strip(),
                    # 'F': row[headers['Customer City']].strip(),
                }
                s_p_c = row[headers['Customer Pincode']].strip()
                s_p_c_id = self.env['pincode.state'].search([('name', '=', s_p_c)])
                if s_p_c_id:
                    customer_vals['zip'] =  s_p_c
                    customer_vals['state_id'] =  s_p_c_id.state_id.id
                    customer_vals['country_id'] =  s_p_c_id.country_id.id
                else:
                    raise UserError(_("The State Pincode"+s_p_c+' is not found. Please Create Pincode in Pincode With State'))
                o_d = datetime.strptime(row[headers['Order Date']].strip(), "%d/%m/%Y")
                inv_d = datetime.strptime(row[headers['Invoice Date']].strip(), "%d/%m/%Y")
                # inv_d = datetime.strptime(row[headers['last-updated-date']].strip(), "%Y-%m-%dT%H:%M:%S%z").date()
                customer_id = self.env['res.partner'].create(customer_vals)
                pro_cat = row[headers['Product Category']].strip()
                if not pro_cat:
                    raise ValidationError('Please enter Product Category Value in sheet.')
                order_vals = {
                    'partner_id': customer_id.id,
                    'order_id': current_order_id,
                    'month_of_sale': self.month_of_sale,
                    'product_cat': pro_cat,
                    'date_order': o_d.utcnow(),
                    'order_date': o_d.date(),
                    # 'is_replacement': True if row[headers['is-replacement-order']].strip().upper() == 'TRUE' else False,
                    # 'original_order_id': row[headers['original-order-id']].strip(),
                    'order_type': row[headers['Order type']].strip(),
                    # 'order_category': 'b2b' if row[headers['is-business-order']].strip().upper() == 'TRUE' else 'b2c',
                    'invoice_no': row[headers['Portal Invoice No.']].strip(),
                    'invoice_date': inv_d,
                    'portal_id': self.env['res.portal'].search([('name', '=', row[headers['Portal Name']].strip())]).id,
                    'order_line': [(0,0, line_vals)],
                }
                w_i = self.env['stock.warehouse'].search([('code', '=', row[headers['Wharehouse']].strip())])
                if w_i:
                    order_vals['warehouse_id'] =  w_i[0].id
                else:
                    raise UserError(_("The Warehouse Code"+w_i+' is not found. Please Create in Inventory as Warehouse'))
                # t_p = self.env['res.partner'].search([('name', '=', row[headers['fulfillment-channel']].strip())])
                # if t_p:
                #     order_vals['third_party'] =  t_p[0].id
                # else:
                #     raise UserError(_("The Third Party "+row[headers['fulfillment-channel']].strip()+' is not found. Please Create in Contects'))
                if line_vals['product_id']:
                    order_create = self.env['sale.order'].create(order_vals)
                else:
                     raise UserError(
                        _(order_vals['order_id']+' is not found. Please Create Product Name'))
            else:
                order_write = order_id.write({'order_line': [(0,0, line_vals)]})
                print("-----------------else-------count----------", count)
            count+=1




############old code 6 feb#############################
    # def do_import(self):
    #     f = base64.b64decode(self.order_file)
    #     data_file = io.StringIO(f.decode("utf-8"))
    #     reader = csv.reader(data_file, delimiter=',')
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     # print("------------headers------", headers)
    #     list_reader = list(reader)
    #     l_reader = len(list_reader)
    #     # print("-------------------#--------", list_reader)
    #     # print("-------------------#--------", l_reader)
    #     if list_reader[1][1] > list_reader[l_reader-1][1]:
    #         # print("------------1----", list_reader[1][1])
    #         # print("------------2----", list_reader[l_reader-1][1])
    #         raise UserError(_('Order Date must be in increasing order.'))
    #     #----------------------------------------------------one-time-check----------------------------------------------------
    #     # count =1
    #     # for row in reader:
    #     #     count+=1
    #     #     if not purchase_date:
    #     #         purchase_date = row[headers['purchase-date']].strip()
    #     #     if purchase_date and purchase_date > row[headers['purchase-date']].strip():
    #     #         raise Warning(_("purchase-date must be in increasing order."))
    #     #     t_p_a = self.env['res.partner'].search([('name', '=', 'Amazon')])
    #     #     t_p_m = self.env['res.partner'].search([('name', '=', 'Merchant')])
    #     #     if not t_p_a:
    #     #         raise Warning(_("fulfillment-channel as 'Amazon' must be in Contects "))
    #     #     if not t_p_m:
    #     #         raise Warning(_("fulfillment-channel as 'Merchant' must be in Contects "))
    #     #     if count >= 4:
    #     #         break
    #     #     print("------------break------")
    #     #----------------------------------------------------check-order----------------------------------------------------
    #     data_file.seek(0)
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     count =2
    #     # print("------------------count--------------", count)
    #     print("------------headers------", headers)
    #     warehouse_ids = self.env['stock.warehouse'].search([])
    #     warehouse_code = [k.code for k in warehouse_ids]
    #     for row in reader:
    #         print("--------------------------------2----------------")
    #         # if row[headers['order-status']].strip() != 'Cancelled' and row[headers['sales-channel']].strip() != 'Non-Amazon' and row[headers['item-status']].strip() != 'Cancelled':
    #         portal_o_id = row[headers['Order ID']].strip()
    #         odoo_o_id = self.env['sale.order'].search([('order_id', '=', portal_o_id)])
    #         print("odoo_o_id....................",odoo_o_id)
    #         if odoo_o_id:
    #             raise UserError(_("Order ID "+portal_o_id+' in line '+str(count)+' is already exists'))
    #         portal_name = row[headers['Portal Name']].strip()
    #         portal_name_id = self.env['res.portal'].search([('name', '=', portal_name)])
    #         if not portal_name_id:
    #             raise UserError(_("Portal Name "+portal_name+' in line '+str(count)+' is not found'))
    #         o_d = row[headers['Order Date']].strip()
    #         order_date = datetime.strptime(o_d, "%d/%m/%Y")
    #         i_d = row[headers['Invoice Date']].strip()
    #         invoice_date = datetime.strptime(i_d, "%d/%m/%Y")
    #         #----------------------------------produt----------------------------
    #         sk = row[headers['sku']].strip()
    #         sk_id = self.env['sku.mapping'].search([('name', '=', sk)])
    #         print("sk_id::::::::::::::::::::", sk_id)
    #         if not sk_id:
    #            raise UserError(_("sku "+sk+' in line '+str(count)+'--in k-id '+portal_o_id+' is not found. create in SKU Mapping'))
    #         fsn = row[headers['FSN']].strip()
    #         fsn_id = self.env['sku.mapping'].search([('id_number', '=', fsn)])
    #         if not fsn_id:
    #             raise UserError(_("fsn "+fsn+' in line '+str(count)+' is not found. update in SKU Mapping'))
    #         # mag = row[headers['Product Magento ID']].strip()
    #         # magento_id = self.env['product.product'].search([('default_code', '=', mag)])
    #         # if not magento_id:
    #         #     raise UserError(_("Product Magento ID "+mag+' in line '+str(count)+'--in Order ID '+portal_o_id+' is not found. create in Product'))
    #         #----------------------------------produt----------------------------
    #         s_p_c = row[headers['Customer Pincode']].strip()
    #         s_p_c_id = self.env['pincode.state'].search([('name', '=', s_p_c)])
    #         if not s_p_c_id:
    #             raise UserError(_("Customer Pincode "+s_p_c+' is not found in line. '+str(count)+' Please Create Pincode in Pincode With State'))
    #         qty = int(row[headers['Quantity']].strip())
    #         portal_price = float(row[headers['Invoice Value Excluding Shipping charges']].strip())
    #         shipping_charges = float(row[headers['Shipping Charges']].strip())
    #         portal_price = float(row[headers['Invoice Value Including Shipping charges']].strip())
    #         # i_r_o = row[headers['is-replacement-order']].strip().upper()
    #         # if i_r_o == 'TRUE' or i_r_o == 'FALSE':
    #         #     pass
    #         # else:
    #         #     raise UserError(_("is-replacement-order must be TRUE or FALSE in line"+str(count)+'--in order-id '+a_o_i))
    #         # if i_r_o == 'TRUE':
    #         #     if not row[headers['original-order-id']].strip():
    #         #         raise UserError(_("original-order-id  order is must in line "+str(count)+'--in order-id '+a_o_i))
    #         # i_b_o = row[headers['is-business-order']].strip().upper()
    #         # if i_b_o == 'TRUE' or i_b_o == 'FALSE':
    #         #     pass
    #         # else:
    #         #     raise UserError(_("is-business-order must be TRUE or FALSE in line"+str(count)+'--in order-id '+a_o_i))
    #         # if i_b_o == 'TRUE':
    #         #     if not row[headers['gstin']].strip():
    #         #         raise UserError(_("gstin number of business order is must in line "+str(count)+'--in order-id '+a_o_i))
    #         #     if len(row[headers['gstin']].strip()) != 15:
    #         #         print("------------gstin------", row[headers['gstin']].strip())
    #         #         print("------------llgstin------", len(row[headers['gstin']].strip()))
    #         #         raise UserError(_("gstin number of business order is must be valid of 15 digits in line "+str(count)+'--in order-id '+a_o_i))
    #         fc = row[headers['Wharehouse']].strip()
    #         if fc not in warehouse_code:
    #             raise Warning(_("Wharehouse "+fc+' is not found. '+' in line '+str(count)+'--in Order ID '+portal_o_id))
    #         print("------------------count--------------", count)
    #         # print("------------------amz_order--------------", row[headers['amazon-order-id']].strip())
    #         count+=1
    #     print("--------------------complete-------------------")
    #     #----------------------------------------------------order-create----------------------------------------------------
    #     data_file.seek(0)
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     print("------------headers------", headers)
    #     count =2
    #     for row in reader:
    #         # if row[headers['order-status']].strip() != 'Cancelled' and row[headers['sales-channel']].strip() != 'Non-Amazon' and row[headers['item-status']].strip() != 'Cancelled':
    #         current_order_id = row[headers['Order ID']].strip()
    #         order_id = self.env['sale.order'].search([('order_id', '=', current_order_id)])
    #         # if order_id:
    #         #     if order_id.state == 'draft':
    #         #         pass
    #         #     else:
    #         #         raise UserError(_("amazon_order_id "+str(current_order_id)+' is already exists with confirmed'))
    #         # if not amazon_order_id or already_amazon_order_id == current_order_id:
    #         #-------------------------------------------product_line------------------------------------------------------------------------------------------------------------------
    #         # sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['sku']].strip())])
    #         # pro_pro_id = self.env['product.product'].search([('default_code', '=', row[headers['sku']].strip())])
    #         sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['sku']].strip())])
    #         line_vals={
    #             'product_uom_qty': int(row[headers['Quantity']].strip()) if row[headers['Quantity']].strip() else 0,
    #             'portal_price': float(row[headers['Invoice Value Excluding Shipping charges']].strip()) if row[headers['Invoice Value Excluding Shipping charges']].strip() else 0.0,
    #             'shipping_charges': float(row[headers['Shipping Charges']].strip()) if row[headers['Shipping Charges']].strip() else 0.0,
    #             # 'portal_price' = float(row[headers['Invoice Value Including Shipping charges']].strip()) if row[headers['Invoice Value Including Shipping charges']].strip() else 0.0
    #         }

    #         # if sk_id:
    #         #     item_price = float(row[headers['item-price']].strip()) if row[headers['item-price']].strip() else 0.0
    #         #     portal_price = item_price/quantity if quantity>=1 else 0.0
    #         #     line_vals['product_id'] = sk_id[0].product_id.id
    #         #     line_vals['name'] = sk_id[0].product_id.name
    #         #     line_vals['sku_id'] = sk_id[0].id
    #         #     line_vals['sku_name'] = sk_id[0].default_code
    #         #     line_vals['portal_price'] = portal_price
    #         if sk_id:
    #             line_vals['product_id'] = sk_id[0].product_id.id
    #             line_vals['name'] = sk_id[0].product_id.name
    #             # line_vals['product_default_code'] = pro_pro_id.default_code
    #             line_vals['sku_id'] = sk_id[0].id
    #             line_vals['sku_name'] = sk_id[0].default_code
    #         else:
    #             raise UserError(_("The Product -----"+row[headers['product-name']].strip()+"----- is  not created yet with ---------"+row[headers['Product Magento ID']].strip()+"----- it should be created first"))
    #         #------------------------------------------------------order-------------------------------------------------------------------------------------------------------
    #         if not order_id:
    #             customer_vals ={
    #                 'name': row[headers['Customer Name']].strip(),
    #                 'street': row[headers['Customer Address']].strip(),
    #                 # 'F': row[headers['Customer City']].strip(),
    #             }
    #             s_p_c = row[headers['Customer Pincode']].strip()
    #             s_p_c_id = self.env['pincode.state'].search([('name', '=', s_p_c)])
    #             if s_p_c_id:
    #                 customer_vals['zip'] =  s_p_c
    #                 customer_vals['state_id'] =  s_p_c_id.state_id.id
    #                 customer_vals['country_id'] =  s_p_c_id.country_id.id
    #             else:
    #                 raise UserError(_("The State Pincode"+s_p_c+' is not found. Please Create Pincode in Pincode With State'))
    #             o_d = datetime.strptime(row[headers['Order Date']].strip(), "%d/%m/%Y")
    #             inv_d = datetime.strptime(row[headers['Invoice Date']].strip(), "%d/%m/%Y")
    #             # inv_d = datetime.strptime(row[headers['last-updated-date']].strip(), "%Y-%m-%dT%H:%M:%S%z").date()
    #             customer_id = self.env['res.partner'].create(customer_vals)
    #             order_vals = {
    #                 'partner_id': customer_id.id,
    #                 'order_id': current_order_id,
    #                 'month_of_sale': self.month_of_sale,
    #                 'date_order': o_d.utcnow(),
    #                 'order_date': o_d.date(),
    #                 # 'is_replacement': True if row[headers['is-replacement-order']].strip().upper() == 'TRUE' else False,
    #                 # 'original_order_id': row[headers['original-order-id']].strip(),
    #                 'order_type': row[headers['Order type']].strip(),
    #                 # 'order_category': 'b2b' if row[headers['is-business-order']].strip().upper() == 'TRUE' else 'b2c',
    #                 'invoice_no': row[headers['Portal Invoice No.']].strip(),
    #                 'invoice_date': inv_d,
    #                 'portal_id': self.env['res.portal'].search([('name', '=', row[headers['Portal Name']].strip())]).id,
    #                 'order_line': [(0,0, line_vals)],
    #             }
    #             w_i = self.env['stock.warehouse'].search([('code', '=', row[headers['Wharehouse']].strip())])
    #             if w_i:
    #                 order_vals['warehouse_id'] =  w_i[0].id
    #             else:
    #                 raise UserError(_("The Warehouse Code"+w_i+' is not found. Please Create in Inventory as Warehouse'))
    #             # t_p = self.env['res.partner'].search([('name', '=', row[headers['fulfillment-channel']].strip())])
    #             # if t_p:
    #             #     order_vals['third_party'] =  t_p[0].id
    #             # else:
    #             #     raise UserError(_("The Third Party "+row[headers['fulfillment-channel']].strip()+' is not found. Please Create in Contects'))
    #             order_create = self.env['sale.order'].create(order_vals)
    #             print("---------------------------count---------------------", count)
    #         else:
    #             order_write = order_id.write({'order_line': [(0,0, line_vals)]})
    #             print("-----------------else-------count----------", count)
    #         count+=1


###########oldcode when sales import with majento id##########################


    # def do_import(self):
    #     f = base64.b64decode(self.order_file)
    #     data_file = io.StringIO(f.decode("utf-8"))
    #     reader = csv.reader(data_file, delimiter=',')
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     # print("------------headers------", headers)
    #     list_reader = list(reader)
    #     l_reader = len(list_reader)
    #     print("-------------------lst--------", list_reader, '--length--', l_reader)
    #     print("-------------------list_reader[0][1]--------", list_reader[0][1])
    #     if list_reader[0][1] > list_reader[l_reader-1][1]:
    #         # print("------------1----", list_reader[1][1])
    #         # print("------------2----", list_reader[l_reader-1][1])
    #         raise UserError(_('Order Date must be in increasing order.'))
    #     #----------------------------------------------------one-time-check----------------------------------------------------
    #     # count =1
    #     # for row in reader:
    #     #     count+=1
    #     #     if not purchase_date:
    #     #         purchase_date = row[headers['purchase-date']].strip()
    #     #     if purchase_date and purchase_date > row[headers['purchase-date']].strip():
    #     #         raise Warning(_("purchase-date must be in increasing order."))
    #     #     t_p_a = self.env['res.partner'].search([('name', '=', 'Amazon')])
    #     #     t_p_m = self.env['res.partner'].search([('name', '=', 'Merchant')])
    #     #     if not t_p_a:
    #     #         raise Warning(_("fulfillment-channel as 'Amazon' must be in Contects "))
    #     #     if not t_p_m:
    #     #         raise Warning(_("fulfillment-channel as 'Merchant' must be in Contects "))
    #     #     if count >= 4:
    #     #         break
    #     #     print("------------break------")
    #     #----------------------------------------------------check-order----------------------------------------------------
    #     data_file.seek(0)
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     count =2
    #     print("------------------count--------------", count)
    #     # print("------------headers------", headers)
    #     warehouse_ids = self.env['stock.warehouse'].search([])
    #     warehouse_code = [k.code for k in warehouse_ids]
    #     for row in reader:
    #         print("--------------------------------2----------------")
    #         # if row[headers['order-status']].strip() != 'Cancelled' and row[headers['sales-channel']].strip() != 'Non-Amazon' and row[headers['item-status']].strip() != 'Cancelled':
    #         portal_o_id = row[headers['Order ID']].strip()
    #         odoo_o_id = self.env['sale.order'].search([('order_id', '=', portal_o_id)])
    #         if odoo_o_id:
    #             raise UserError(_("Order ID "+portal_o_id+' in line '+str(count)+' is already exists'))
    #         portal_name = row[headers['Portal Name']].strip()
    #         portal_name_id = self.env['res.portal'].search([('name', '=', portal_name)])
    #         if not portal_name_id:
    #             raise UserError(_("Portal Name "+portal_name+' in line '+str(count)+' is not found'))
    #         o_d = row[headers['Order Date']].strip()
    #         order_date = datetime.strptime(o_d, "%d/%m/%Y")
    #         i_d = row[headers['Invoice Date']].strip()
    #         invoice_date = datetime.strptime(i_d, "%d/%m/%Y")
    #         #----------------------------------produt----------------------------
    #         # sk = row[headers['Product Magento ID']].strip()
    #         # sk_id = self.env['sku.mapping'].search([('name', '=', sk)])
    #         # if not sk_id:
    #         #     raise UserError(_("sku "+sk+' in line '+str(count)+'--in k-id '+portal_o_id+' is not found. create in SKU Mapping'))
    #         # asin = row[headers['asin']].strip()
    #         # asin_id = self.env['sku.mapping'].search([('id_number', '=', asin)])
    #         # if not asin_id:
    #         #     raise UserError(_("asin "+asin+' in line '+str(count)+' is not found. update in SKU Mapping'))
    #         mag = row[headers['Product Magento ID']].strip()
    #         magento_id = self.env['product.product'].search([('default_code', '=', mag)])
    #         if not magento_id:
    #             raise UserError(_("Product Magento ID "+mag+' in line '+str(count)+'--in Order ID '+portal_o_id+' is not found. create in Product'))
    #         #----------------------------------produt----------------------------
    #         s_p_c = row[headers['Customer Pincode']].strip()
    #         s_p_c_id = self.env['pincode.state'].search([('name', '=', s_p_c)])
    #         if not s_p_c_id:
    #             raise UserError(_("Customer Pincode "+s_p_c+' is not found in line. '+str(count)+' Please Create Pincode in Pincode With State'))
    #         qty = int(row[headers['Quantity']].strip())
    #         portal_price = float(row[headers['Invoice Value Excluding Shipping charges']].strip())
    #         shipping_charges = float(row[headers['Shipping Charges']].strip())
    #         portal_price = float(row[headers['Invoice Value Including Shipping charges']].strip())
    #         # i_r_o = row[headers['is-replacement-order']].strip().upper()
    #         # if i_r_o == 'TRUE' or i_r_o == 'FALSE':
    #         #     pass
    #         # else:
    #         #     raise UserError(_("is-replacement-order must be TRUE or FALSE in line"+str(count)+'--in order-id '+a_o_i))
    #         # if i_r_o == 'TRUE':
    #         #     if not row[headers['original-order-id']].strip():
    #         #         raise UserError(_("original-order-id  order is must in line "+str(count)+'--in order-id '+a_o_i))
    #         # i_b_o = row[headers['is-business-order']].strip().upper()
    #         # if i_b_o == 'TRUE' or i_b_o == 'FALSE':
    #         #     pass
    #         # else:
    #         #     raise UserError(_("is-business-order must be TRUE or FALSE in line"+str(count)+'--in order-id '+a_o_i))
    #         # if i_b_o == 'TRUE':
    #         #     if not row[headers['gstin']].strip():
    #         #         raise UserError(_("gstin number of business order is must in line "+str(count)+'--in order-id '+a_o_i))
    #         #     if len(row[headers['gstin']].strip()) != 15:
    #         #         print("------------gstin------", row[headers['gstin']].strip())
    #         #         print("------------llgstin------", len(row[headers['gstin']].strip()))
    #         #         raise UserError(_("gstin number of business order is must be valid of 15 digits in line "+str(count)+'--in order-id '+a_o_i))
    #         fc = row[headers['Wharehouse']].strip()
    #         if fc not in warehouse_code:
    #             raise Warning(_("Wharehouse "+fc+' is not found. '+' in line '+str(count)+'--in Order ID '+portal_o_id))
    #         print("------------------count--------------", count)
    #         # print("------------------amz_order--------------", row[headers['amazon-order-id']].strip())
    #         count+=1
    #     print("--------------------complete-------------------")
    #     #----------------------------------------------------order-create----------------------------------------------------
    #     data_file.seek(0)
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     print("------------headers------", headers)
    #     count =2
    #     for row in reader:
    #         # if row[headers['order-status']].strip() != 'Cancelled' and row[headers['sales-channel']].strip() != 'Non-Amazon' and row[headers['item-status']].strip() != 'Cancelled':
    #         current_order_id = row[headers['Order ID']].strip()
    #         order_id = self.env['sale.order'].search([('order_id', '=', current_order_id)])
    #         # if order_id:
    #         #     if order_id.state == 'draft':
    #         #         pass
    #         #     else:
    #         #         raise UserError(_("amazon_order_id "+str(current_order_id)+' is already exists with confirmed'))
    #         # if not amazon_order_id or already_amazon_order_id == current_order_id:
    #         #-------------------------------------------product_line------------------------------------------------------------------------------------------------------------------
    #         # sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['sku']].strip())])
    #         pro_pro_id = self.env['product.product'].search([('default_code', '=', row[headers['Product Magento ID']].strip())])
    #         line_vals={
    #             'product_uom_qty': int(row[headers['Quantity']].strip()) if row[headers['Quantity']].strip() else 0,
    #             'portal_price': float(row[headers['Invoice Value Excluding Shipping charges']].strip()) if row[headers['Invoice Value Excluding Shipping charges']].strip() else 0.0,
    #             'shipping_charges': float(row[headers['Shipping Charges']].strip()) if row[headers['Shipping Charges']].strip() else 0.0,
    #             # 'portal_price' = float(row[headers['Invoice Value Including Shipping charges']].strip()) if row[headers['Invoice Value Including Shipping charges']].strip() else 0.0
    #         }
    #         if pro_pro_id:
    #             line_vals['product_id'] = pro_pro_id.id
    #             line_vals['name'] = pro_pro_id.name
    #             line_vals['product_default_code'] = pro_pro_id.default_code
    #             # line_vals['sku_id'] = sk_id[0].id
    #             # line_vals['sku_name'] = sk_id[0].default_code
    #         else:
    #             raise UserError(_("The Product -----"+row[headers['product-name']].strip()+"----- is  not created yet with ---------"+row[headers['Product Magento ID']].strip()+"----- it should be created first"))
    #         #------------------------------------------------------order-------------------------------------------------------------------------------------------------------
    #         if not order_id:
    #             customer_vals ={
    #                 'name': row[headers['Customer Name']].strip(),
    #                 'street': row[headers['Customer Address']].strip(),
    #                 'city': row[headers['Customer City']].strip(),
    #             }
    #             s_p_c = row[headers['Customer Pincode']].strip()
    #             s_p_c_id = self.env['pincode.state'].search([('name', '=', s_p_c)])
    #             if s_p_c_id:
    #                 customer_vals['zip'] =  s_p_c
    #                 customer_vals['state_id'] =  s_p_c_id.state_id.id
    #                 customer_vals['country_id'] =  s_p_c_id.country_id.id
    #             else:
    #                 raise UserError(_("The State Pincode"+s_p_c+' is not found. Please Create Pincode in Pincode With State'))
    #             o_d = datetime.strptime(row[headers['Order Date']].strip(), "%d/%m/%Y")
    #             inv_d = datetime.strptime(row[headers['Invoice Date']].strip(), "%d/%m/%Y")
    #             # inv_d = datetime.strptime(row[headers['last-updated-date']].strip(), "%Y-%m-%dT%H:%M:%S%z").date()
    #             customer_id = self.env['res.partner'].create(customer_vals)
    #             order_vals = {
    #                 'partner_id': customer_id.id,
    #                 'order_id': current_order_id,
    #                 'month_of_sale': self.month_of_sale,
    #                 'date_order': o_d.utcnow(),
    #                 'order_date': o_d.date(),
    #                 # 'is_replacement': True if row[headers['is-replacement-order']].strip().upper() == 'TRUE' else False,
    #                 # 'original_order_id': row[headers['original-order-id']].strip(),
    #                 'order_type': row[headers['Order type']].strip(),
    #                 # 'order_category': 'b2b' if row[headers['is-business-order']].strip().upper() == 'TRUE' else 'b2c',
    #                 'invoice_no': row[headers['Portal Invoice No.']].strip(),
    #                 'invoice_date': inv_d,
    #                 'portal_id': self.env['res.portal'].search([('name', '=', row[headers['Portal Name']].strip())]).id,
    #                 'order_line': [(0,0, line_vals)],
    #             }
    #             w_i = self.env['stock.warehouse'].search([('code', '=', row[headers['Wharehouse']].strip())])
    #             if w_i:
    #                 order_vals['warehouse_id'] =  w_i[0].id
    #             else:
    #                 raise UserError(_("The Warehouse Code"+w_i+' is not found. Please Create in Inventory as Warehouse'))
    #             # t_p = self.env['res.partner'].search([('name', '=', row[headers['fulfillment-channel']].strip())])
    #             # if t_p:
    #             #     order_vals['third_party'] =  t_p[0].id
    #             # else:
    #             #     raise UserError(_("The Third Party "+row[headers['fulfillment-channel']].strip()+' is not found. Please Create in Contects'))
    #             order_create = self.env['sale.order'].create(order_vals)
    #             print("---------------------------count---------------------", count)
    #         else:
    #             order_write = order_id.write({'order_line': [(0,0, line_vals)]})
    #             print("-----------------else-------count----------", count)
    #         count+=1

    # def gst_mtr_b2b_warehouse_update(self):
    #     f = base64.b64decode(self.order_file)
    #     data_file = io.StringIO(f.decode("utf-8"))
    #     reader = csv.reader(data_file, delimiter=',')
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     count =1
    #     for row in reader:
    #         order_id = self.env['sale.order'].search([('order_id', '=', row[headers['Order Id']].strip())])
    #         # print("-----------order_id-------", order_id)
    #         wh_code = row[headers['Warehouse Id']].strip()
    #         if order_id and order_id.state == 'draft':
    #             wh_id = self.env['stock.warehouse'].search([('code', '=', wh_code)])
    #             # print("-----------------wh_id----", wh_id)
    #             if wh_code and wh_id and order_id.warehouse_id.code == 'WH':
    #                 wh_update = order_id.write({'warehouse_id': wh_id[0].id})
    #                 # print("------------wh_id-------", wh_id.name)
    #                 # print("------------wh_update-------", wh_update)
    #             # else:
    #             #     raise Warning(_("The Warehouse "+wh_code+' is not found. Please Create in Inventory as Warehouse'))
    #             if not order_id.partner_id.vat:
    #                 gstn_no = row[headers['Customer Bill To Gstid']].strip()
    #                 if gstn_no:
    #                     order_id.partner_id.write({'vat': gstn_no})
    #                     order_id.write({'order_category': 'b2b'})
    #             partner_name = row[headers['Buyer Name']].strip()
    #             if partner_name:
    #                 order_id.partner_id.write({'name': partner_name})
    #         count+=1
    #         print("-----------------count----------", count)

    # def gst_mtr_b2c_warehouse_update(self):
    #     f = base64.b64decode(self.order_file)
    #     data_file = io.StringIO(f.decode("utf-8"))
    #     reader = csv.reader(data_file, delimiter=',')
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     count =1
    #     for row in reader:
    #         order_id = self.env['sale.order'].search([('order_id', '=', row[headers['Order Id']].strip())])
    #         if order_id.warehouse_id.code == 'WH':
    #             # print("-----------order_id-------", order_id)
    #             wh_code = row[headers['Warehouse Id']].strip()
    #             if order_id and order_id.state == 'draft':
    #                 wh_id = self.env['stock.warehouse'].search([('code', '=', wh_code)])
    #                 # print("-----------------wh_id----", wh_id)
    #                 if wh_code and wh_id:
    #                     wh_update = order_id.write({'warehouse_id': wh_id[0].id})
    #                     # print("------------wh_id-------", wh_id.name)
    #                     # print("------------wh_update-------", wh_update)
    #                 # else:
    #                 #     raise Warning(_("The Warehouse "+wh_code+' is not found. Please Create in Inventory as Warehouse'))
    #         count+=1
    #         print("-----------------count----------", count)

    # def shipment_warehouse_update(self):
    #     f = base64.b64decode(self.order_file)
    #     data_file = io.StringIO(f.decode("utf-8"))
    #     reader = csv.reader(data_file, delimiter=',')
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     # print("------------headers------", headers)
    #     count =1
    #     for row in reader:
    #         print("----------o---------", row[headers['FC']].strip())
    #         a_o_i = row[headers['Amazon Order Id']].strip()
    #         # print("----------a_o_i--------", a_o_i)
    #         order_id = self.env['sale.order'].search([('order_id', '=', a_o_i)])
    #         if order_id.warehouse_id.code == 'WH':
    #             # print("-----------order_id-------", order_id)
    #             wh_code = row[headers['FC']].strip()
    #             if order_id and order_id.state == 'draft':
    #                 wh_id = self.env['stock.warehouse'].search([('code', '=', row[headers['FC']].strip())])
    #                 if wh_code and wh_id:
    #                     wh_update = order_id.write({'warehouse_id': wh_id[0].id})
    #                     # print("------------wh_id-------", wh_id.code)
    #                     # print("------------wh_update-------", wh_update)
    #                 # else:
    #                 #     raise Warning(_("The Warehouse "+wh_code+' is not found. Please Create in Inventory as Warehouse'))
    #         count+=1
    #         print("-----------------count----------", count)


    # def Not_do_import(self):
    #     f = base64.b64decode(self.order_file)
    #     data_file = io.StringIO(f.decode("utf-8"))
    #     reader = csv.reader(data_file, delimiter=',')
        
    #     headers = {}
    #     for row in reader:
    #         col_count = 0
    #         for col in row:
    #             headers[col] = col_count
    #             col_count = col_count + 1
    #         break;
    #     count =1
    #     already_order_id = ''
    #     already_so_id = ''

    #     if self.order_b2b_b2c == 'b2c':
    #         for row in reader:
    #             order_id = row[headers['order-id']].strip() if row[headers['order-id']].strip() else ''
    #             if order_id != already_order_id:
    #                 already_order_id = order_id
    #                 customer_vals ={
    #                     'name': row[headers['Customer-name-shipping']].strip(),
    #                     'street': row[headers['address-shipping']].strip(),
    #                     'city': row[headers['city-shipping']].strip(),
    #                     # 'state_id': self.env['res.country.state'].search([('name', '=', row[headers['State-shipping']]), ('country_id', '=', 104)])[0].id,
    #                     'zip': row[headers['pincode-shipping']].strip(),
    #                 }
    #                 state_ids = self.env['res.country.state'].search([('name', '=', row[headers['State-shipping']].strip()), ('country_id', '=', 104)])
    #                 if state_ids:
    #                     customer_vals['state_id'] =  state_ids[0].id
    #                     customer_vals['country_id'] =  104
    #                 else:
    #                     raise Warning(_("The State "+row[headers['State-shipping']].strip()+' is not found. Please Create state in Fed. state'))
    #                     # self.env['sale.order.missing'].create({'channel_name': row[headers['sales-channel']].strip(), 'order_no': order_id, 'sku_name': row[headers['sku-id']].strip(), 'reason': 'The State '+row[headers['State-shipping']].strip()+' is not found. Please Create state in Fed. state'})
    #                     # count = count+1
    #                     # print("---------------------count-------------------", count)
    #                     # continue
    #                 customer_id = self.env['res.partner'].create(customer_vals)
    #                 # d_o = datetime.strptime(row[headers['order-date']].strip(), "%d-%b-%y")
    #                 d_o = datetime.strptime(row[headers['order-date']].strip(), "%d/%m/%y")
    #                 o_d = datetime.strptime(row[headers['order-date']].strip(), "%d/%m/%y").date()
    #                 # inv_d = datetime.strptime(row[headers['Invoice Date']].strip(), "%d-%b-%y").date()
    #                 inv_d = datetime.strptime(row[headers['order-date']].strip(), "%d/%m/%y").date()
    #                 # inv_d = datetime.strptime(row[headers['Invoice Date']].strip(), "%d/%m/%y").date()
    #                 order_vals = {
    #                     'partner_id': customer_id.id,
    #                     'order_id': order_id,
    #                     'date_order': d_o,
    #                     'order_date': o_d,
    #                     'order_type': row[headers['fulfillment-channel']].strip(),
    #                     'order_category': self.order_b2b_b2c,
    #                     'invoice_no': row[headers['Invoice No.']].strip(),
    #                     'invoice_date': inv_d,
    #                     # 'tracking_no': row[headers['tracking id']].strip(),
    #                     # 'delivery_partner_name': row[headers['Delivery partner']].strip()
    #                 }
    #                 t_p = self.env['res.partner'].search([('name', '=', row[headers['sales-channel']].strip())])
    #                 if t_p:
    #                     order_vals['third_party'] =  t_p[0].id
    #                 else:
    #                     raise Warning(_("The Third Party "+row[headers['sales-channel']].strip()+' is not found. Please Create in Contects as Customer'))
    #                 w_i = self.env['stock.warehouse'].search([('name', '=', row[headers['warehouse']].strip())])
    #                 if w_i:
    #                     order_vals['warehouse_id'] =  w_i[0].id
    #                 else:
    #                     raise Warning(_("The Warehouse "+row[headers['warehouse']].strip()+' is not found. Please Create in Inventory as Warehouse'))
    #                 sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['sku-id']].strip())])
    #                 if sk_id:
    #                     order_vals['order_line'] = [(0,0,{'product_id': sk_id[0].product_id.id, 'name': sk_id[0].product_id.name, 'sku_id': sk_id[0].id, 'sku_name': sk_id[0].default_code, 'product_uom_qty': row[headers['quantity']].strip(), 'portal_price': float( row[headers['item-unit-price']].strip()), 'shipping_charges': row[headers['unit-shipping-charges']].strip()})]
    #                 else:
    #                     raise Warning(_("The Product -----"+row[headers['product-name']].strip()+"----- has not been map with ---------"+row[headers['sku-id']].strip()+"----- please create SKU ID of product"))
    #                 order_create = self.env['sale.order'].create(order_vals)
    #                 already_so_id = order_create
    #                 print("------------------order_create-------------", order_create)
    #                 count = count+1
    #                 print("---------------------------count---------------------", count)
    #             else:
    #                 sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['sku-id']].strip())])
    #                 if sk_id:
    #                     order_write = already_so_id.write({'order_line': [(0,0,{'product_id': sk_id.product_id.id, 'name': sk_id.product_id.name, 'sku_id': sk_id.id, 'sku_name': sk_id.name, 'name': sk_id.product_id.name, 'product_uom_qty': row[headers['quantity']].strip(), 'portal_price': float( row[headers['item-unit-price']].strip()), 'shipping_charges': row[headers['unit-shipping-charges']].strip()})]})
    #                     print("-----------------order_write--------------", order_write)
    #                     count = count+1
    #                     print("-----------------else-------count----------", count)
    #                 else:
    #                     raise Warning(_("The Product -----"+row[headers['product-name']]+"----- has not been map with ---------"+row[headers['sku-id']].strip()+"----- please create SKU ID of product"))

    #     if self.order_b2b_b2c == 'b2b':
    #         print("-----------------yes-------b2b----")
    #         already_order_id = ''
    #         already_so_id = ''
    #         for row in reader:
    #             order_id = row[headers['PO']].strip() if row[headers['PO']].strip() else ''
    #             if order_id is not already_order_id:
    #                 already_order_id = order_id
    #                 d_o = datetime.strptime(row[headers['PO Date']].strip(), "%d/%m/%Y")
    #                 order_vals = {
    #                     'hg_party_id': row[headers['HG Party ID']].strip(),
    #                     'order_id': order_id,
    #                     'date_order': d_o,
    #                     'order_type': row[headers['Third party']].strip(),
    #                     'order_category': self.order_b2b_b2c
    #                 }
    #                 t_p = self.env['res.partner'].search([('name', '=', row[headers['Third party']].strip())])
    #                 if t_p:
    #                     order_vals['third_party'] =  t_p[0].id
    #                     order_vals['partner_id'] =  t_p[0].id
    #                 else:
    #                     raise Warning(_("The Third Party "+row[headers['Third party']].strip()+' is not found. Please Create in Contects as Customer'))
    #                 w_i = self.env['stock.warehouse'].search([('fs', '=', row[headers['Warehouse']].strip())])
    #                 if w_i:
    #                     order_vals['warehouse_id'] =  w_i[0].id
    #                 else:
    #                     raise Warning(_("The Warehouse "+row[headers['Warehouse']].strip()+' is not found. Please Create in Inventory as Warehouse'))
    #                 sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['SKU']].strip())])
    #                 if sk_id:
    #                     order_vals['order_line'] = [(0,0,{'product_id': sk_id[0].product_id.id, 'name': sk_id[0].product_id.name, 'sku_id': sk_id[0].id, 'sku_name': sk_id[0].name, 'name': sk_id[0].product_id.name, 'product_uom_qty': row[headers['Quantity']].strip(), 'price_unit': row[headers['Cost']].strip()})]
    #                 else:
    #                     # self.env['sale.order.missing'].create({'channel_name': row[headers['sales-channel']], 'order_no': order_id, 'sku_name': row[headers['sku-id']], })
    #                     raise Warning(_("The Product -----"+row[headers['Title']].strip()+"----- has not been map with ---------"+row[headers['SKU']].strip()+"----- please create SKU ID of product"))
    #                 order_create = self.env['sale.order'].create(order_vals)
    #                 already_so_id = order_create
    #                 print("------------------order_create-------------", order_create)
    #                 count = count+1
    #                 print("-----------------count----------------------", count)
    #             else:
    #                 sk_id = self.env['sku.mapping'].search([('name', '=', row[headers['SKU']].strip())])
    #                 if sk_id:
    #                     order_write = already_so_id.write({'order_line': [(0,0,{'product_id': sk_id.product_id.id, 'name': sk_id.product_id.name, 'sku_id': sk_id.id, 'sku_name': sk_id.name, 'name': sk_id.product_id.name, 'product_uom_qty': row[headers['Quantity']].strip(), 'price_unit': row[headers['Cost']].strip()})]})
    #                     print("-----------------order_write--------------", order_write)
    #                     count = count+1
    #                     print("++++++++++++++++++count++++++++++++++++++", count)
    #                 else:
    #                     raise Warning(_("The Product -----"+row[headers['Title']].strip()+"----- has not been map with ---------"+row[headers['SKU']].strip()+"----- please create SKU ID of product"))
