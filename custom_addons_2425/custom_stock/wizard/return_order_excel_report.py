# -*- coding: utf-8 -*-
import xlwt
import base64
import calendar
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
from textwrap import wrap

class ReturnOrderXls(models.TransientModel):
    _name = "return.order.xls"
    _description = 'Return Order Xls'
    return_order_category = fields.Selection([('b2b', 'B2B'), ('b2c', 'B2C')], string="Return Order(B2B/B2C)")
    month_of_return = fields.Selection([
        ('all_month', 'All Month'),
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
        ], string="Month of Return", default=False, required=True)
    start_date = fields.Date(string='Date From')
    end_date = fields.Date(string='Date To')
    warehouse_id = fields.Many2one('stock.warehouse', string="To Warehouse")
    file_name = fields.Char('Name', size=256)
    file_xls = fields.Binary(' Report', readonly=True)
    flag = fields.Boolean(string="Flag")

    def action_return_order_xls(self):
        print("============aaction_b2b_report================")
        workbook = xlwt.Workbook()
        ws = workbook.add_sheet('Sheet1')
        s_h = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center")
        print("---------------------------------writting into sheet--------------------")
        if self.month_of_return:
            ws.write(0, 0, 'Date', s_h)
            ws.write(0, 1, 'Sale Order Number', s_h)
            ws.write(0, 2, 'Invoice number', s_h)
            ws.write(0, 3, 'Channel entry', s_h)
            ws.write(0, 4, 'Channel Ledger', s_h)
            ws.write(0, 5, 'Product Name', s_h)
            ws.write(0, 6, 'Product SKU Code', s_h)
            ws.write(0, 7, 'Qty', s_h)
            ws.write(0, 8, 'Unit Price', s_h)
            ws.write(0, 9, 'Currency', s_h)
            ws.write(0, 10, 'Conversion Rate', s_h)
            ws.write(0, 11, 'Total', s_h)
            ws.write(0, 12, 'Customer Name', s_h)
            ws.write(0, 13, 'Shipping Address Name', s_h)
            ws.write(0, 14, 'Shipping Address Line 1', s_h)
            ws.write(0, 15, 'Shipping Address Line 2', s_h)
            ws.write(0, 16, 'Shipping Address City', s_h)
            ws.write(0, 17, 'Shipping Address State', s_h)
            ws.write(0, 18, 'Shipping Address Country', s_h)
            ws.write(0, 19, 'Shipping Address Pincode', s_h)
            ws.write(0, 20, 'Shipping Address Phone', s_h)
            ws.write(0, 21, 'Shipping Provider', s_h)
            ws.write(0, 22, 'AWB num', s_h)
            ws.write(0, 23, 'Sales', s_h)
            ws.write(0, 24, 'Sales Ledger', s_h)
            # ws.write(0, 25, 'Tax Rate', s_h)555555555555555555555555
            # ws.write(0, 26, 'Tax Sum', s_h)666666666666666666666666
            ws.write(0, 25, 'CGST', s_h)
            ws.write(0, 26, 'CGST Rate', s_h)
            ws.write(0, 27, 'SGST', s_h)
            ws.write(0, 28, 'SGST Rate', s_h)
            ws.write(0, 29, 'IGST', s_h)
            ws.write(0, 30, 'IGST Rate', s_h)
            ws.write(0, 31, 'UTGST', s_h)
            ws.write(0, 32, 'UTGST Rate', s_h)
            ws.write(0, 33, 'CESS', s_h)
            ws.write(0, 34, 'CESS Rate', s_h)
            ws.write(0, 35, 'Other charges', s_h)
            ws.write(0, 36, 'Other charges Ledger', s_h)
            ws.write(0, 37, 'Other charges1', s_h)
            ws.write(0, 38, 'Other charges Ledger1', s_h)
            ws.write(0, 39, 'Service tax', s_h)
            ws.write(0, 40, 'ST Ledger', s_h)
            ws.write(0, 41, 'IMEI', s_h)
            ws.write(0, 42, 'Godown', s_h)
            ws.write(0, 43, 'Dispatch Date/Cancellation Date', s_h)
            ws.write(0, 44, 'Narration', s_h)
            ws.write(0, 45, 'Entity', s_h)
            ws.write(0, 46, 'Voucher Type Name', s_h)
            ws.write(0, 47, 'TIN NO', s_h)
            ws.write(0, 48, 'Original Invoice Date', s_h)
            ws.write(0, 49, 'Original Sale No', s_h)
            ws.write(0, 50, 'odoo order no', s_h)
            ws.write(0, 51, 'Suborder no', s_h)
            ws.write(0, 52, 'HSN', s_h)

            ws.write(0, 53, 'GSTIN Seller', s_h)
            ws.write(0, 54, 'Sale From State', s_h)
            ws.write(0, 55, 'GSTIN Buyer', s_h)
            ws.write(0, 56, 'POS', s_h)
            ws.write(0, 57, 'Tax Rate', s_h)
            ws.write(0, 58, 'Tax Sum', s_h)

            ws.write(0, 59, 'Status', s_h)
            # ws.write(0, 56, 'GSTIN Buyer', s_h)3333333333333333333
            ws.write(0, 60, 'Company Name', s_h)
            # ws.write(0, 58, 'GSTIN Seller', s_h)111111111111111111111
            # ws.write(0, 59, 'POS', s_h)4444444444444444444444
            # ws.write(0, 60, 'Sale From State', s_h)22222222222222222
            ws.write(0, 61, 'Sale From Warehouse(ID)', s_h)
            ws.write(0, 62, 'Original Order', s_h)
            ws.write(0, 63, 'Shipping Charges', s_h)
            ws.write(0, 64, 'Gift Wrap Price', s_h)
            ws.write(0, 65, 'Promotional Discount', s_h)
            ws.write(0, 66, 'RTO Reason', s_h)
            ws.write(0, 67, 'Return Order No.', s_h)
            ws.write(0, 68, 'Other Portal Name.', s_h)
            return_vals = []
            if self.month_of_return:
                return_vals.append(('month_of_return', '=', self.month_of_return))
            if self.start_date and self.end_date:
                return_vals.append(('return_date', '>=', self.start_date))
                return_vals.append(('return_date', '<=', self.end_date))
            if self.warehouse_id:
                return_vals.append(('warehouse_id', '=', self.warehouse_id.id))
            return_ids = self.env['return.order'].search(return_vals, order='id asc')
            # print("-------------return_ids--------------", return_ids)
            if return_ids:
                row = 1
                for rto in return_ids:
                    if rto:
                        ws.write(row, 0, rto.return_date.strftime("%d-%m-%Y"))
                        # ws.write(row, 1, rto.invoice_order_id.sale_number)
                        ws.write(row, 1, rto.invoice_order_id.invoice_number)

                        ws.write(row, 2, rto.name)
                        ws.write(row, 3, rto.invoice_order_id.portal_id.name)
                        ws.write(row, 4, rto.invoice_order_id.portal_id.name)
                        ws.write(row, 5, rto.product_product_id.name)
                        ws.write(row, 6, rto.product_product_id.default_code)
                        ws.write(row, 7, rto.quntity)
                        ws.write(row, 8, rto.price_unit)
                        ws.write(row, 9, 'INR')
                        ws.write(row, 10, 1)
                        ws.write(row, 11, rto.grand_subtotal)
                        ws.write(row, 12, 'Online Sale Through Pay. Rec. by Flipkart (HI)')
                        ws.write(row, 13, rto.invoice_order_id.partner_id.name)
                        ws.write(row, 14, '')
                        ws.write(row, 15, '')
                        ws.write(row, 16, rto.invoice_order_id.partner_id.city)
                        ws.write(row, 17, rto.invoice_order_id.partner_id.state_id.name)
                        # ws.write(row, 17, rto.invoice_order_id.partner_id.state_id.l10n_in_tin+'-'+rto.invoice_order_id.partner_id.state_id.name)
                        ws.write(row, 18, rto.invoice_order_id.partner_id.country_id.name)
                        ws.write(row, 19, rto.invoice_order_id.partner_id.zip)
                        ws.write(row, 20, '')
                        ws.write(row, 21, '')
                        ws.write(row, 22, '')
                        ws.write(row, 23,
                                 rto.price_subtotal + rto.shipping_charges_basic + rto.gift_wrap_basic - rto.item_promo_discount_basic)
                        # change sanjeev
                        ws.write(row, 24, 'CGST+SGST Sale-' + 'B2C' + '-' + str(int(rto.tax_ids[0].amount)) + '%' if rto.invoice_order_id.partner_id.state_id.name == rto.invoice_order_id.warehouse_id.state_id.name else 'IGST Sale-' + 'B2C' + '-' + str(int(rto.tax_ids[0].amount)) + '%')
                        # ws.write(row, 24, 'CGST+SGST Sale-' + 'B2C' + '-' + str(rto.invoice_order_id.order_category).upper()+'-'+str(int(rto.tax_ids[0].amount)) + '%' if rto.invoice_order_id.partner_id.name == rto.invoice_order_id.warehouse_id.name else 'IGST Sale-' + 'B2C' + '-' + str(int(rto.tax_ids[0].amount)) + '%')
                        ws.write(row, 25, rto.cgst_amount)
                        ws.write(row, 26,'B2C-Output Tax CGST' if rto.invoice_order_id.partner_id.state_id.name == rto.invoice_order_id.warehouse_id.state_id.name else '')
                        # ws.write(row, 24, 'CGST+SGST Sale-'+str(rto.invoice_order_id.order_category).upper()+'-'+str(int(rto.tax_ids[0].amount))+'%' if rto.invoice_order_id.partner_id.vat[0:2] == rto.invoice_order_id.warehouse_id.gstin[0:2] else 'IGST Sale-'+str(rto.invoice_order_id.order_category).upper()+'-'+str(int(rto.tax_ids[0].amount))+'%')
                        # ws.write(row, 25, rto.tax_sum)55555555555555555555555555
                        total_cgst = rto.cgst_amount + rto.shipping_charges_cgst + rto.gift_wrap_cgst - rto.item_promo_cgst
                        total_sgst = rto.sgst_amount + rto.shipping_charges_sgst + rto.gift_wrap_sgst - rto.item_promo_sgst
                        total_igst = rto.igst_amount + rto.shipping_charges_igst + rto.gift_wrap_igst - rto.item_promo_igst
                        # ws.write(row, 26, total_cgst+total_sgst+total_igst)666666666666666666666666
                        # ws.write(row, 25, total_cgst)
                        cgst = rto.tax_ids[0].amount / 2 if (rto.tax_ids[0].amount / 2) % 1 > 0.0 else int(
                            rto.tax_ids[0].amount / 2)
                        # ws.write(row, 26, 'Output Tax -CGST@ '+str(cgst)+'%' if rto.invoice_order_id.partner_id.vat[0:2] == rto.invoice_order_id.warehouse_id.gstin[0:2] else '')
                        ws.write(row, 27, total_sgst)
                        # sanjeev change
                        # ws.write(row, 28, 'B2C-Output Tax -CGST@ '+ str(rto.sgst_rate))
                        ws.write(row, 28,
                                 'B2C-Output Tax SGST' if rto.invoice_order_id.partner_id.state_id.name == rto.invoice_order_id.warehouse_id.state_id.name else '')
                        ws.write(row, 29, total_igst)
                        ws.write(row, 30,
                                 'B2C-Output Tax IGST' if rto.invoice_order_id.partner_id.state_id.name != rto.invoice_order_id.warehouse_id.state_id.name else '')
                        # ws.write(row, 30, 'Output Tax -IGST@ '+str(int(rto.tax_ids[0].amount))+'%' if rto.invoice_order_id.partner_id.vat[0:2] != rto.invoice_order_id.warehouse_id.gstin[0:2] else '')
                        ws.write(row, 31, '')
                        ws.write(row, 32, '')
                        ws.write(row, 33, '')
                        ws.write(row, 34, '')
                        ws.write(row, 35, '')
                        ws.write(row, 36, '')
                        ws.write(row, 37, '')
                        ws.write(row, 38, '')
                        ws.write(row, 39, '')
                        ws.write(row, 40, '')
                        ws.write(row, 41, '')
                        ws.write(row, 42, rto.warehouse_id.name)
                        ws.write(row, 43, '')
                        # ws.write(row, 44, 'Being order id '+str(rto.invoice_order_id.so_id.sale_number_b2b)+' Invoice no '+str(rto.invoice_order_id.invoice_number_b2b)+' suborder id '+str(rto.invoice_order_id.order_id)+' sale through '+str(rto.invoice_order_id.order_type)+' customer name '+str(rto.invoice_order_id.partner_id.name)+' state '+str(rto.invoice_order_id.partner_id.state_id.name)+' Godown '+str(rto.invoice_order_id.warehouse_id.name)+' GSTIN '+str(rto.invoice_order_id.partner_id.vat)+' Company Name '+str(rto.invoice_order_id.partner_id.name))
                        ws.write(row, 45, 'NEW INVOICE')
                        ws.write(row, 46, 'Sale Return(Ok)')
                        # ws.write(row, 46, 'Sales Return(Ok)-B2B' if rto.invoice_order_id.partner_id.vat[0:2] == rto.invoice_order_id.warehouse_id.gstin[0:2] else 'Sale-IGST-B2B')
                        ws.write(row, 47, '')
                        ws.write(row, 48, rto.invoice_order_id.invoice_date.strftime("%d-%m-%Y"))
                        ws.write(row, 49, rto.invoice_order_id.invoice_number)
                        ws.write(row, 50, rto.invoice_order_id.sale_number)
                        ws.write(row, 51, rto.portal_order_id)
                        ws.write(row, 52, rto.product_product_id.l10n_in_hsn_code)

                        ws.write(row, 53, rto.invoice_order_id.warehouse_id.gstin)
                        # ws.write(row, 54, rto.invoice_order_id.warehouse_id.state_id.l10n_in_tin+'-'+rto.invoice_order_id.warehouse_id.state_id.name)
                        ws.write(row, 54, rto.from_warehouse_id.state_id.name)
                        ws.write(row, 55, rto.invoice_order_id.partner_id.vat)
                        # ws.write(row, 56, rto.invoice_order_id.partner_id.vat[0:2]+'-'+self.env['res.country.state'].search([('country_id', '=', 104), ('l10n_in_tin', '=', rto.invoice_order_id.partner_id.vat[0:2])]).name)
                        ws.write(row, 57, rto.tax_sum)
                        # total_cgst = rto.cgst_amount+rto.shipping_charges_cgst+rto.gift_wrap_cgst-rto.item_promo_cgst
                        # total_sgst = rto.sgst_amount+rto.shipping_charges_sgst+rto.gift_wrap_sgst-rto.item_promo_sgst
                        # total_igst = rto.igst_amount+rto.shipping_charges_igst+rto.gift_wrap_igst-rto.item_promo_igst
                        ws.write(row, 58, total_cgst + total_sgst + total_igst)

                        ws.write(row, 59, 'Return')
                        # ws.write(row, 53, 'INVOICED' if rto.invoice_order_id.state == 'posted' else '')
                        # ws.write(row, 56, rto.invoice_order_id.partner_id.vat)33333333333333333333333
                        ws.write(row, 60, rto.invoice_order_id.partner_id.name)
                        # # ws.write(row, 58, rto.invoice_order_id.warehouse_id.gstin)1111111111111111
                        # # ws.write(row, 59, rto.invoice_order_id.partner_id.vat[0:2]+'-'+self.env['res.country.state'].search([('country_id', '=', 104), ('l10n_in_tin', '=', rto.invoice_order_id.partner_id.vat[0:2])]).name)444444444444444444444444444
                        # # ws.write(row, 60, rto.invoice_order_id.warehouse_id.state_id.name)222222222222222222222222222
                        ws.write(row, 61, rto.from_warehouse_id.code)
                        ws.write(row, 62, rto.invoice_order_id.original_order_id)
                        ws.write(row, 63, rto.shipping_charges)
                        ws.write(row, 64, rto.gift_wrap_price)
                        ws.write(row, 65, rto.item_promo_discount)
                        ws.write(row, 66, rto.return_reason)
                        ws.write(row, 67, rto.return_o_no)
                        ws.write(row, 68, rto.invoice_order_id.portal_id.name)
                        row += 1
                    else:
                        ws.write(row, 0, rto.return_date.strftime("%d-%m-%Y"))
                        # ws.write(row, 1, rto.odoo_order_b2b)
                        ws.write(row, 2, rto.name)
                        ws.write(row, 3, rto.invoice_order_id.portal_id.name)
                        ws.write(row, 4, rto.invoice_order_id.portal_id.name)
                        ws.write(row, 5, rto.product_product_id.name)
                        ws.write(row, 6, rto.product_product_id.default_code)
                        ws.write(row, 7, rto.quntity)
                        ws.write(row, 8, rto.price_unit)
                        ws.write(row, 9, 'INR')
                        ws.write(row, 10, 1)
                        ws.write(row, 11, rto.grand_subtotal)
                        ws.write(row, 12, 'Online Sale Through Pay. Rec. by Flipkart (HI)')
                        ws.write(row, 13, rto.partner_name)
                        ws.write(row, 14, '')
                        ws.write(row, 15, '')
                        ws.write(row, 16, rto.partner_city)
                        # ws.write(row, 17, rto.state_id.name)
                        ws.write(row, 17, rto.state_id.l10n_in_tin+'-'+rto.state_id.name)
                        ws.write(row, 18, rto.country_id.name)
                        ws.write(row, 19, rto.partner_zip_code)
                        ws.write(row, 20, '')
                        ws.write(row, 21, '')
                        ws.write(row, 22, '')
                        ws.write(row, 23, rto.price_subtotal+rto.shipping_charges_basic+rto.gift_wrap_basic-rto.item_promo_discount_basic)
                        ws.write(row, 24, 'CGST+SGST Sale-'+str(rto.order_category).upper()+'-'+str(int(rto.tax_ids[0].amount))+'%' if rto.partner_vat[0:2] == rto.from_warehouse_id.gstin[0:2] else 'IGST Sale-'+str(rto.order_category).upper()+'-'+str(int(rto.tax_ids[0].amount))+'%')
                        # ws.write(row, 25, rto.tax_sum)5555555555555555555555555
                        total_cgst = rto.cgst_amount+rto.shipping_charges_cgst+rto.gift_wrap_cgst-rto.item_promo_cgst
                        total_sgst = rto.sgst_amount+rto.shipping_charges_sgst+rto.gift_wrap_sgst-rto.item_promo_sgst
                        total_igst = rto.igst_amount+rto.shipping_charges_igst+rto.gift_wrap_igst-rto.item_promo_igst
                        # ws.write(row, 26, total_cgst+total_sgst+total_igst)66666666666666666666666666666
                        ws.write(row, 25, total_cgst)
                        cgst = rto.tax_ids[0].amount/2 if (rto.tax_ids[0].amount/2)%1>0.0 else int(rto.tax_ids[0].amount/2)
                        ws.write(row, 26, 'Output Tax -CGST@ '+str(cgst)+'%' if rto.partner_vat[0:2] == rto.from_warehouse_id.gstin[0:2] else '')
                        ws.write(row, 27, total_sgst)
                        ws.write(row, 28, 'Output Tax -SGST@ '+str(cgst)+'%' if rto.partner_vat[0:2] == rto.from_warehouse_id.gstin[0:2] else '')
                        ws.write(row, 29, total_igst)
                        ws.write(row, 30, 'Output Tax -IGST@ '+str(int(rto.tax_ids[0].amount))+'%' if rto.partner_vat[0:2] != rto.from_warehouse_id.gstin[0:2] else '')
                        ws.write(row, 31, '')
                        ws.write(row, 32, '')
                        ws.write(row, 33, '')
                        ws.write(row, 34, '')
                        ws.write(row, 35, '')
                        ws.write(row, 36, '')
                        ws.write(row, 37, '')
                        ws.write(row, 48, '')
                        ws.write(row, 39, '')
                        ws.write(row, 40, '')
                        ws.write(row, 41, '')
                        ws.write(row, 42, rto.warehouse_id.name)
                        ws.write(row, 43, '')
                        ws.write(row, 44, 'Being order id '+str(rto.sale_number_b2b)+' Invoice no '+str(rto.odoo_order_b2b)+' suborder id '+str(rto.portal_order_id)+' sale through '+'Amazon'+' customer name '+str(rto.partner_name)+' state '+str(rto.state_id.name)+' Godown '+str(rto.from_warehouse_id.name)+' GSTIN '+str(rto.partner_vat)+' Company Name '+str(rto.partner_name))
                        ws.write(row, 45, 'NEW INVOICE')
                        ws.write(row, 46, 'Sales Return(Ok)-B2B')
                        # ws.write(row, 46, 'Sales Return(Ok)-B2B' if rto.invoice_order_id.partner_id.vat[0:2] == rto.invoice_order_id.warehouse_id.gstin[0:2] else 'Sale-IGST-B2B')
                        ws.write(row, 47, '')
                        ws.write(row, 48, rto.invoice_date.strftime("%d-%m-%Y") if rto.invoice_date else '')
                        ws.write(row, 49, rto.odoo_order_b2b)
                        ws.write(row, 50, rto.sale_number_b2b)
                        ws.write(row, 51, rto.portal_order_id)
                        ws.write(row, 52, rto.product_product_id.l10n_in_hsn_code)

                        ws.write(row, 53, rto.from_warehouse_id.gstin)
                        ws.write(row, 54, rto.from_warehouse_id.state_id.l10n_in_tin+'-'+rto.from_warehouse_id.state_id.name)
                        ws.write(row, 55, rto.partner_vat)
                        ws.write(row, 56, rto.partner_vat[0:2]+'-'+self.env['res.country.state'].search([('country_id', '=', 104), ('l10n_in_tin', '=', rto.partner_vat[0:2])]).name)
                        ws.write(row, 57, rto.tax_sum)
                        # total_cgst = rto.cgst_amount+rto.shipping_charges_cgst+rto.gift_wrap_cgst-rto.item_promo_cgst
                        # total_sgst = rto.sgst_amount+rto.shipping_charges_sgst+rto.gift_wrap_sgst-rto.item_promo_sgst
                        # total_igst = rto.igst_amount+rto.shipping_charges_igst+rto.gift_wrap_igst-rto.item_promo_igst
                        ws.write(row, 58, total_cgst+total_sgst+total_igst)


                        ws.write(row, 59, 'Return')
                        # ws.write(row, 53, 'INVOICED' if rto.invoice_order_id.state == 'posted' else '')
                        # ws.write(row, 56, rto.partner_vat)33333333333333333333
                        ws.write(row, 60, rto.partner_name)
                        # ws.write(row, 58, rto.from_warehouse_id.gstin)1111111111111111111
                        # ws.write(row, 59, rto.partner_vat[0:2]+'-'+self.env['res.country.state'].search([('country_id', '=', 104), ('l10n_in_tin', '=', rto.partner_vat[0:2])]).name)44444444444444444444
                        # ws.write(row, 60, rto.from_warehouse_id.state_id.name)2222222222222222222222222222
                        ws.write(row, 61, rto.from_warehouse_id.code)
                        ws.write(row, 62, rto.original_order_id)
                        ws.write(row, 63, rto.shipping_charges)
                        ws.write(row, 64, rto.gift_wrap_price)
                        ws.write(row, 65, rto.item_promo_discount)
                        ws.write(row, 66, rto.return_reason)
                        ws.write(row, 67, rto.return_reason)
                        ws.write(row, 68, rto.invoice_order_id.portal_id.name)
                        row+=1    
            else:
                raise Warning("Currently No Return Order For B2C in This Data!!")
            filename = '/tmp/Return_Order_B2B'+'.xls'
            workbook.save(filename)
            file = open(filename, "rb")
            file_data = file.read()
            out = base64.encodebytes(file_data)
            self.write({'file_name': filename, 'file_xls':out, 'flag': True})
            return {
               'type': 'ir.actions.act_window',
               'res_model': 'return.order.xls',
               'view_mode': 'form',
               'view_type': 'form',
               'res_id': self.id,
               'target': 'new',
            }


        # if self.return_order_category == 'b2c':
        #     ws.write(0, 0, 'Date', s_h)
        #     ws.write(0, 1, 'Sale Order Number', s_h)
        #     ws.write(0, 2, 'Invoice number', s_h)
        #     ws.write(0, 3, 'Channel entry', s_h)
        #     ws.write(0, 4, 'Channel Ledger', s_h)
        #     ws.write(0, 5, 'Product Name', s_h)
        #     ws.write(0, 6, 'Product SKU Code', s_h)
        #     ws.write(0, 7, 'Qty', s_h)
        #     ws.write(0, 8, 'Unit Price', s_h)
        #     ws.write(0, 9, 'Currency', s_h)
        #     ws.write(0, 10, 'Conversion Rate', s_h)
        #     ws.write(0, 11, 'Total', s_h)
        #     ws.write(0, 12, 'Customer Name', s_h)
        #     ws.write(0, 13, 'Shipping Address Name', s_h)
        #     ws.write(0, 14, 'Shipping Address Line 1', s_h)
        #     ws.write(0, 15, 'Shipping Address Line 2', s_h)
        #     ws.write(0, 16, 'Shipping Address City', s_h)
        #     ws.write(0, 17, 'Shipping Address State', s_h)
        #     ws.write(0, 18, 'Shipping Address Country', s_h)
        #     ws.write(0, 19, 'Shipping Address Pincode', s_h)
        #     ws.write(0, 20, 'Shipping Address Phone', s_h)
        #     ws.write(0, 21, 'Shipping Provider', s_h)
        #     ws.write(0, 22, 'AWB num', s_h)
        #     ws.write(0, 23, 'Sales', s_h)
        #     ws.write(0, 24, 'Sales Ledger', s_h)
        #     # ws.write(0, 25, 'Tax Rate', s_h)555555555555555555
        #     # ws.write(0, 26, 'Tax Sum', s_h)666666666666666666666
        #     ws.write(0, 25, 'CGST', s_h)
        #     ws.write(0, 26, 'CGST Rate', s_h)
        #     ws.write(0, 27, 'SGST', s_h)
        #     ws.write(0, 28, 'SGST Rate', s_h)
        #     ws.write(0, 29, 'IGST', s_h)
        #     ws.write(0, 30, 'IGST Rate', s_h)
        #     ws.write(0, 31, 'UTGST', s_h)
        #     ws.write(0, 32, 'UTGST Rate', s_h)
        #     ws.write(0, 33, 'CESS', s_h)
        #     ws.write(0, 34, 'CESS Rate', s_h)
        #     ws.write(0, 35, 'Other charges', s_h)
        #     ws.write(0, 36, 'Other charges Ledger', s_h)
        #     ws.write(0, 37, 'Other charges1', s_h)
        #     ws.write(0, 38, 'Other charges Ledger1', s_h)
        #     ws.write(0, 39, 'Service tax', s_h)
        #     ws.write(0, 40, 'ST Ledger', s_h)
        #     ws.write(0, 41, 'IMEI', s_h)
        #     ws.write(0, 42, 'Godown', s_h)
        #     ws.write(0, 43, 'Dispatch Date/Cancellation Date', s_h)
        #     ws.write(0, 44, 'Narration', s_h)
        #     ws.write(0, 45, 'Entity', s_h)
        #     ws.write(0, 46, 'Voucher Type Name', s_h)
        #     ws.write(0, 47, 'TIN NO', s_h)
        #     ws.write(0, 48, 'Original Invoice Date', s_h)
        #     ws.write(0, 49, 'Original Sale No', s_h)
        #     ws.write(0, 50, 'odoo order no', s_h)
        #     ws.write(0, 51, 'Suborder no', s_h)
        #     ws.write(0, 52, 'HSN', s_h)

        #     ws.write(0, 53, 'GSTIN Seller', s_h)
        #     ws.write(0, 54, 'Sale From State', s_h)
        #     ws.write(0, 55, 'GSTIN Buyer', s_h)
        #     ws.write(0, 56, 'POS', s_h)
        #     ws.write(0, 57, 'Tax Rate', s_h)
        #     ws.write(0, 58, 'Tax Sum', s_h)


        #     ws.write(0, 59, 'Status', s_h)
        #     # ws.write(0, 55, 'GSTIN Buyer', s_h)333333333333333333333
        #     # ws.write(0, 56, 'Company Name', s_h)
        #     # ws.write(0, 56, 'GSTIN Seller', s_h)11111111111111111111111111111
        #     # ws.write(0, 57, 'POS', s_h)444444444444444444444444444
        #     # ws.write(0, 58, 'Sale From State', s_h)222222222222222222
        #     ws.write(0, 60, 'Sale From Warehouse(ID)', s_h)
        #     ws.write(0, 61, 'Original Order', s_h)
        #     ws.write(0, 62, 'Shipping Charges', s_h)
        #     ws.write(0, 63, 'Gift Wrap Price', s_h)
        #     ws.write(0, 64, 'Promotional Discount', s_h)
        #     ws.write(0, 65, 'RTO Reason', s_h)
        #     return_vals = [('order_category', '=', 'b2c')]
        #     if self.month_of_return:
        #         return_vals.append(('month_of_return', '=', self.month_of_return))
        #     if self.start_date and self.end_date:
        #         return_vals.append(('return_date', '>=', self.start_date))
        #         return_vals.append(('return_date', '<=', self.end_date))
        #     if self.warehouse_id:
        #         return_vals.append(('warehouse_id', '=', self.warehouse_id.id))
        #     return_ids = self.env['return.order'].search(return_vals, order='id asc')
        #     # print("-------------return_ids--------------", return_ids)
        #     if return_ids:
        #         row = 1
        #         for rto in return_ids:
        #             if rto.invoice_line_id:
        #                 ws.write(row, 0, rto.return_date.strftime("%d-%m-%Y"))
        #                 ws.write(row, 1, rto.invoice_order_id.invoice_number)
        #                 ws.write(row, 2, rto.name)
        #                 ws.write(row, 3, 'Online Sale Through Pay. Rec. by Amazon (HI)')
        #                 ws.write(row, 4, 'Online Sale Through Pay. Rec. by Amazon (HI)')
        #                 ws.write(row, 5, rto.product_product_id.name)
        #                 ws.write(row, 6, rto.product_product_id.default_code)
        #                 ws.write(row, 7, rto.quntity)
        #                 ws.write(row, 8, rto.price_unit)
        #                 ws.write(row, 9, 'INR')
        #                 ws.write(row, 10, 1)
        #                 ws.write(row, 11, rto.grand_subtotal)
        #                 ws.write(row, 12, 'Online Sale Through Pay. Rec. by Amazon (HI)')
        #                 ws.write(row, 13, rto.invoice_order_id.partner_id.name)
        #                 ws.write(row, 14, '')
        #                 ws.write(row, 15, '')
        #                 ws.write(row, 16, rto.invoice_order_id.partner_id.city)
        #                 ws.write(row, 17, rto.invoice_order_id.partner_id.state_id.l10n_in_tin+'-'+rto.invoice_order_id.partner_id.state_id.name)
        #                 ws.write(row, 18, rto.invoice_order_id.partner_id.country_id.name)
        #                 ws.write(row, 19, rto.invoice_order_id.partner_id.zip)
        #                 ws.write(row, 20, '')
        #                 ws.write(row, 21, '')
        #                 ws.write(row, 22, '')
        #                 ws.write(row, 23, rto.price_subtotal+rto.shipping_charges_basic+rto.gift_wrap_basic-rto.item_promo_discount_basic)
        #                 ws.write(row, 24, 'CGST+SGST Sale-'+str(rto.invoice_order_id.order_category).upper()+'-'+str(int(rto.tax_ids[0].amount))+'%' if rto.invoice_order_id.partner_id.state_id.id == rto.invoice_order_id.warehouse_id.state_id.id else 'IGST Sale-'+str(rto.invoice_order_id.order_category).upper()+'-'+str(int(rto.tax_ids[0].amount))+'%')
        #                 # ws.write(row, 25, rto.tax_sum)55555555555555555555555555
        #                 total_cgst = rto.cgst_amount+rto.shipping_charges_cgst+rto.gift_wrap_cgst-rto.item_promo_cgst
        #                 total_sgst = rto.sgst_amount+rto.shipping_charges_sgst+rto.gift_wrap_sgst-rto.item_promo_sgst
        #                 cgst = rto.tax_ids[0].amount/2 if (rto.tax_ids[0].amount/2)%1>0.0 else int(rto.tax_ids[0].amount/2)
        #                 total_igst = rto.igst_amount+rto.shipping_charges_igst+rto.gift_wrap_igst-rto.item_promo_igst
        #                 # ws.write(row, 26, total_cgst+total_sgst+total_igst)6666666666666666666666
        #                 ws.write(row, 25, total_cgst)
        #                 ws.write(row, 26, 'B2C-Output Tax -CGST@ '+str(cgst)+'%' if rto.invoice_order_id.partner_id.state_id.id == rto.invoice_order_id.warehouse_id.state_id.id else '')
        #                 ws.write(row, 27, total_sgst)
        #                 ws.write(row, 28, 'B2C-Output Tax -SGST@ '+str(cgst)+'%' if rto.invoice_order_id.partner_id.state_id.id == rto.invoice_order_id.warehouse_id.state_id.id else '')
        #                 ws.write(row, 29, total_igst)
        #                 ws.write(row, 30, 'B2C-Output Tax -IGST@ '+str(int(rto.tax_ids[0].amount))+'%' if rto.invoice_order_id.partner_id.state_id.id != rto.invoice_order_id.warehouse_id.state_id.id else '')
        #                 ws.write(row, 31, '')
        #                 ws.write(row, 32, '')
        #                 ws.write(row, 33, '')
        #                 ws.write(row, 34, '')
        #                 ws.write(row, 35, '')
        #                 ws.write(row, 36, '')
        #                 ws.write(row, 37, '')
        #                 ws.write(row, 38, '')
        #                 ws.write(row, 39, '')
        #                 ws.write(row, 40, '')
        #                 ws.write(row, 41, '')
        #                 ws.write(row, 42, rto.warehouse_id.name)
        #                 ws.write(row, 43, '')
        #                 ws.write(row, 44, 'Being order id '+str(rto.invoice_order_id.so_id.sale_number)+' Invoice no '+str(rto.invoice_order_id.invoice_number)+' suborder id '+str(rto.invoice_order_id.order_id)+' sale through '+str(rto.invoice_order_id.order_type)+' customer name '+str(rto.invoice_order_id.partner_id.name)+' state '+str(rto.invoice_order_id.partner_id.state_id.name)+' Godown '+str(rto.invoice_order_id.warehouse_id.name)+' GSTIN '+str(rto.invoice_order_id.partner_id.vat)+' Company Name '+str(rto.invoice_order_id.partner_id.name))
        #                 ws.write(row, 45, 'NEW INVOICE')
        #                 ws.write(row, 46, 'Sales Return(Ok)-B2C')
        #                 # ws.write(row, 46, 'Sales Return(Ok)-B2B' if rto.invoice_order_id.partner_id.vat[0:2] == rto.invoice_order_id.warehouse_id.gstin[0:2] else 'Sale-IGST-B2B')
        #                 ws.write(row, 47, '')
        #                 ws.write(row, 48, rto.invoice_order_id.invoice_date.strftime("%d-%m-%Y"))
        #                 ws.write(row, 49, rto.invoice_order_id.invoice_number)
        #                 ws.write(row, 50, rto.invoice_order_id.sale_number)
        #                 ws.write(row, 51, rto.portal_order_id)
        #                 ws.write(row, 52, rto.product_product_id.l10n_in_hsn_code)

        #                 ws.write(row, 53, rto.invoice_order_id.warehouse_id.gstin)
        #                 ws.write(row, 54, rto.invoice_order_id.warehouse_id.state_id.l10n_in_tin+'-'+rto.invoice_order_id.warehouse_id.state_id.name)
        #                 ws.write(row, 55, rto.invoice_order_id.partner_id.name)
        #                 ws.write(row, 56, rto.invoice_order_id.partner_id.state_id.l10n_in_tin+'-'+rto.invoice_order_id.partner_id.state_id.name)
        #                 ws.write(row, 57, rto.tax_sum)
        #                 # total_cgst = rto.cgst_amount+rto.shipping_charges_cgst+rto.gift_wrap_cgst-rto.item_promo_cgst
        #                 # total_sgst = rto.sgst_amount+rto.shipping_charges_sgst+rto.gift_wrap_sgst-rto.item_promo_sgst
        #                 # cgst = rto.tax_ids[0].amount/2 if (rto.tax_ids[0].amount/2)%1>0.0 else int(rto.tax_ids[0].amount/2)
        #                 # total_igst = rto.igst_amount+rto.shipping_charges_igst+rto.gift_wrap_igst-rto.item_promo_igst
        #                 ws.write(row, 58, total_cgst+total_sgst+total_igst)


        #                 ws.write(row, 59, 'Return')
        #                 # ws.write(row, 53, 'INVOICED' if rto.invoice_order_id.state == 'posted' else '')
        #                 # ws.write(row, 55, rto.invoice_order_id.partner_id.vat)33333333333333333333333
        #                 # ws.write(row, 56, rto.invoice_order_id.partner_id.name)
        #                 # ws.write(row, 60, rto.invoice_order_id.warehouse_id.gstin)1111111111111111111111
        #                 # ws.write(row, 57, rto.invoice_order_id.partner_id.state_id.l10n_in_tin+'-'+rto.invoice_order_id.partner_id.state_id.name)44444444444444444
        #                 # ws.write(row, 58, rto.invoice_order_id.warehouse_id.state_id.name)2222222222222222222
        #                 ws.write(row, 60, rto.from_warehouse_id.code)
        #                 ws.write(row, 61, rto.invoice_order_id.original_order_id)
        #                 ws.write(row, 62, rto.shipping_charges)
        #                 ws.write(row, 63, rto.gift_wrap_price)
        #                 ws.write(row, 64, rto.item_promo_discount)
        #                 ws.write(row, 65, rto.return_reason)
        #                 row+=1
        #             else:
        #                 ws.write(row, 0, rto.return_date.strftime("%d-%m-%Y"))
        #                 ws.write(row, 1, rto.odoo_order_b2c)
        #                 ws.write(row, 2, rto.name)
        #                 ws.write(row, 3, 'Online Sale Through Pay. Rec. by Amazon (HI)')
        #                 ws.write(row, 4, 'Online Sale Through Pay. Rec. by Amazon (HI)')
        #                 ws.write(row, 5, rto.product_product_id.name)
        #                 ws.write(row, 6, rto.product_product_id.default_code)
        #                 ws.write(row, 7, rto.quntity)
        #                 ws.write(row, 8, rto.price_unit)
        #                 ws.write(row, 9, 'INR')
        #                 ws.write(row, 10, 1)
        #                 ws.write(row, 11, rto.grand_subtotal)
        #                 ws.write(row, 12, 'Online Sale Through Pay. Rec. by Amazon (HI)')
        #                 ws.write(row, 13, rto.partner_name)
        #                 ws.write(row, 14, '')
        #                 ws.write(row, 15, '')
        #                 ws.write(row, 16, rto.partner_city)
        #                 ws.write(row, 17, rto.state_id.l10n_in_tin+'-'+rto.state_id.name)
        #                 ws.write(row, 18, rto.country_id.name)
        #                 ws.write(row, 19, rto.partner_zip_code)
        #                 ws.write(row, 20, '')
        #                 ws.write(row, 21, '')
        #                 ws.write(row, 22, '')
        #                 ws.write(row, 23, rto.price_subtotal+rto.shipping_charges_basic+rto.gift_wrap_basic-rto.item_promo_discount_basic)
        #                 ws.write(row, 24, 'CGST+SGST Sale-'+str(rto.order_category).upper()+'-'+str(int(rto.tax_ids[0].amount))+'%' if rto.state_id.id == rto.from_warehouse_id.state_id.id else 'IGST Sale-'+str(rto.order_category).upper()+'-'+str(int(rto.tax_ids[0].amount))+'%')
        #                 # ws.write(row, 25, rto.tax_sum)5555555555555555555555555
        #                 cgst = rto.tax_ids[0].amount/2 if (rto.tax_ids[0].amount/2)%1>0.0 else int(rto.tax_ids[0].amount/2)
        #                 total_cgst = rto.cgst_amount+rto.shipping_charges_cgst+rto.gift_wrap_cgst-rto.item_promo_cgst
        #                 total_sgst = rto.sgst_amount+rto.shipping_charges_sgst+rto.gift_wrap_sgst-rto.item_promo_sgst
        #                 total_igst = rto.igst_amount+rto.shipping_charges_igst+rto.gift_wrap_igst-rto.item_promo_igst
        #                 # ws.write(row, 26, total_cgst+total_sgst+total_igst)666666666666666666666666
        #                 ws.write(row, 25, total_cgst)
        #                 ws.write(row, 26, 'B2C-Output Tax -CGST@ '+str(cgst)+'%' if rto.state_id.id == rto.from_warehouse_id.state_id.id else '')
        #                 ws.write(row, 27, total_sgst)
        #                 ws.write(row, 28, 'B2C-Output Tax -SGST@ '+str(cgst)+'%' if rto.state_id.id == rto.from_warehouse_id.state_id.id else '')
        #                 ws.write(row, 29, total_igst)
        #                 ws.write(row, 30, 'B2C-Output Tax -IGST@ '+str(int(rto.tax_ids[0].amount))+'%' if rto.state_id.id != rto.from_warehouse_id.state_id.id else '')
        #                 ws.write(row, 31, '')
        #                 ws.write(row, 32, '')
        #                 ws.write(row, 33, '')
        #                 ws.write(row, 34, '')
        #                 ws.write(row, 35, '')
        #                 ws.write(row, 36, '')
        #                 ws.write(row, 37, '')
        #                 ws.write(row, 38, '')
        #                 ws.write(row, 39, '')
        #                 ws.write(row, 40, '')
        #                 ws.write(row, 41, '')
        #                 ws.write(row, 42, rto.warehouse_id.name)
        #                 ws.write(row, 43, '')
        #                 ws.write(row, 44, 'Being order id '+str(rto.sale_number)+' Invoice no '+str(rto.odoo_order_b2c)+' suborder id '+str(rto.portal_order_id)+' sale through '+'Amazon'+' customer name '+str(rto.partner_name)+' state '+str(rto.state_id.name)+' Godown '+str(rto.from_warehouse_id.name)+' GSTIN '+str(rto.partner_vat)+' Company Name '+str(rto.partner_name))
        #                 ws.write(row, 45, 'NEW INVOICE')
        #                 ws.write(row, 46, 'Sales Return(Ok)-B2C')
        #                 # ws.write(row, 46, 'Sales Return(Ok)-B2B' if rto.invoice_order_id.partner_id.vat[0:2] == rto.invoice_order_id.warehouse_id.gstin[0:2] else 'Sale-IGST-B2B')
        #                 ws.write(row, 47, '')
        #                 ws.write(row, 48, rto.invoice_date.strftime("%d-%m-%Y") if rto.invoice_date else '')
        #                 ws.write(row, 49, rto.odoo_order_b2c)
        #                 ws.write(row, 50, rto.sale_number)
        #                 ws.write(row, 51, rto.portal_order_id)
        #                 ws.write(row, 52, rto.product_product_id.l10n_in_hsn_code)

        #                 ws.write(row, 53, rto.from_warehouse_id.gstin)
        #                 ws.write(row, 54, rto.from_warehouse_id.state_id.l10n_in_tin+'-'+rto.from_warehouse_id.state_id.name)
        #                 ws.write(row, 55, rto.partner_name)
        #                 ws.write(row, 56, rto.state_id.l10n_in_tin+'-'+rto.state_id.name)
        #                 ws.write(row, 57, rto.tax_sum)
        #                 # cgst = rto.tax_ids[0].amount/2 if (rto.tax_ids[0].amount/2)%1>0.0 else int(rto.tax_ids[0].amount/2)
        #                 # total_cgst = rto.cgst_amount+rto.shipping_charges_cgst+rto.gift_wrap_cgst-rto.item_promo_cgst
        #                 # total_sgst = rto.sgst_amount+rto.shipping_charges_sgst+rto.gift_wrap_sgst-rto.item_promo_sgst
        #                 # total_igst = rto.igst_amount+rto.shipping_charges_igst+rto.gift_wrap_igst-rto.item_promo_igst
        #                 ws.write(row, 58, total_cgst+total_sgst+total_igst)


        #                 ws.write(row, 59, 'Return')
        #                 # ws.write(row, 53, 'INVOICED' if rto.invoice_order_id.state == 'posted' else '')
        #                 # ws.write(row, 56, rto.from_warehouse_id.gstin)111111111111111111
        #                 # ws.write(row, 57, rto.state_id.l10n_in_tin+'-'+rto.state_id.name)4444444444444444444444444444
        #                 # ws.write(row, 58, rto.from_warehouse_id.state_id.name)2222222222222222222222
        #                 ws.write(row, 60, rto.from_warehouse_id.code)
        #                 ws.write(row, 61, rto.original_order_id)
        #                 ws.write(row, 62, rto.shipping_charges)
        #                 ws.write(row, 63, rto.gift_wrap_price)
        #                 ws.write(row, 64, rto.item_promo_discount)
        #                 ws.write(row, 65, rto.return_reason)
        #                 row+=1
        #     else:
        #         raise Warning("Currently No Return Order For B2C in This Data!!")
        #     filename = '/tmp/Return_Order_B2C'+'.xls'
        #     workbook.save(filename)
        #     file = open(filename, "rb")
        #     file_data = file.read()
        #     out = base64.encodestring(file_data)
        #     self.write({'file_name': filename, 'file_xls':out, 'flag': True})
        #     return {
        #        'type': 'ir.actions.act_window',
        #        'res_model': 'return.order.xls',
        #        'view_mode': 'form',
        #        'view_type': 'form',
        #        'res_id': self.id,
        #        'target': 'new',
        #     }
