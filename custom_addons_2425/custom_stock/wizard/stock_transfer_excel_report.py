# -*- coding: utf-8 -*-
import xlwt
import base64
import calendar
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
from textwrap import wrap

class StockTranferSaleXls(models.TransientModel):
    _name = "stock.transfer.sale.xls"
    _description = 'Stock Tranfer Sale Xls'
    month_of_stock_trns = fields.Selection([
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
        ], string="Month of Stock Tranfer", required=True)
    ship_from_fc = fields.Many2one('stock.warehouse', string="Ship From Fc")
    file_name = fields.Char('Name', size=256)
    file_xls = fields.Binary(' Report', readonly=True)
    flag = fields.Boolean(string="Flag")

    def action_stock_tranfer_sale_xls(self):
        print("============action_stock_tranfer_sale_xls================")
        workbook = xlwt.Workbook()
        ws = workbook.add_sheet('Sheet1')
        s_h = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center")
        print("---------------------------------writting into sheet--------------------")
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
        ws.write(0, 10, 'conversion rate', s_h)
        ws.write(0, 11, 'Total', s_h)
        ws.write(0, 12, 'Customer Name', s_h)
        ws.write(0, 13, 'Shipping Address Name', s_h)
        ws.write(0, 14, 'Shipping Address Line 1', s_h)
        ws.write(0, 15, 'Shipping Address Line 2', s_h)
        ws.write(0, 16, 'Shipping Address City', s_h)
        ws.write(0, 17, 'Shipping Address State', s_h)
        ws.write(0, 18, 'Country', s_h)
        ws.write(0, 19, 'Shipping Address Pincode', s_h)
        ws.write(0, 20, 'Shipping Address Phone', s_h)
        ws.write(0, 21, 'Shipping Provider', s_h)
        ws.write(0, 22, 'AWB num', s_h)
        ws.write(0, 23, 'Sales', s_h)
        ws.write(0, 24, 'Sales Ledger', s_h)
        ws.write(0, 25, 'CGST', s_h)
        ws.write(0, 26, 'CGST Rate.', s_h)
        ws.write(0, 27, 'SGST', s_h)
        ws.write(0, 28, 'SGST Rate.', s_h)
        ws.write(0, 29, 'IGST', s_h)
        ws.write(0, 30, 'IGST Rate.', s_h)
        ws.write(0, 31, 'UTGST', s_h)
        ws.write(0, 32, 'UTGST Rate.', s_h)
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
        ws.write(0, 52, 'HSN Code', s_h)
        ws.write(0, 53, 'Units', s_h)
        ws.write(0, 54, 'Category', s_h)
        ws.write(0, 55, 'GST of Supplier', s_h)
        ws.write(0, 56, 'GST of Buyer', s_h)
        ws.write(0, 57, 'State of Supplier', s_h)
        ws.write(0, 58, 'Product ASIN', s_h)
        ws.write(0, 59, 'Transaction Type', s_h)
        stock_t_sale_ids = None
        if self.month_of_stock_trns == 'all_month':
            if not self.ship_from_fc:
                print("---------------------1-------------")
                stock_t_sale_ids = self.env['stock.transfer.sale'].search([], order='id asc')
        if self.month_of_stock_trns != 'all_month':
            if not self.ship_from_fc:
                print("---------------------2-------------")
                stock_t_sale_ids = self.env['stock.transfer.sale'].search([('month_of_stock_trns', '=', self.month_of_stock_trns)], order='id asc')
        if self.month_of_stock_trns == 'all_month':
            if self.ship_from_fc:
                print("---------------------3-------------")
                stock_t_sale_ids = self.env['stock.transfer.sale'].search([('ship_from_fc', '=', self.ship_from_fc.id)], order='id asc')
        if self.month_of_stock_trns != 'all_month':
            if self.ship_from_fc:
                print("---------------------4-------------")
                stock_t_sale_ids = self.env['stock.transfer.sale'].search([('month_of_stock_trns', '=', self.month_of_stock_trns), ('ship_from_fc', '=', self.ship_from_fc.id)], order='id asc')
        # print("-------------invoice_ids--------------", stock_t_sale_ids)
        if stock_t_sale_ids:
            row = 1
            for sts in stock_t_sale_ids:
                for sts_l in sts.stock_transfer_line: 
                    ws.write(row, 0, sts.invoice_date.strftime("%d-%m-%Y"))
                    ws.write(row, 1, sts.name)
                    ws.write(row, 2, sts.name)
                    ws.write(row, 3, 'Br.Sinew Nutrition Private Ltd ('+wrap(sts.ship_from_fc.gstin, 2)[0]+'+'+wrap(sts.ship_to_fc.gstin, 2)[0]+')')
                    ws.write(row, 4, 'Br.Sinew Nutrition Private Ltd ('+wrap(sts.ship_from_fc.gstin, 2)[0]+'+'+wrap(sts.ship_to_fc.gstin, 2)[0]+')')
                    ws.write(row, 5, sts_l.product_product_id.name)
                    ws.write(row, 6, sts_l.default_code)
                    ws.write(row, 7, sts_l.quntity)
                    ws.write(row, 8, sts_l.unit_price)
                    ws.write(row, 9, '')
                    ws.write(row, 10, '')
                    ws.write(row, 11, sts_l.invoice_vales)
                    ws.write(row, 12, 'Br.Sinew Nutrition Private Ltd ('+wrap(sts.ship_from_fc.gstin, 2)[0]+'+'+wrap(sts.ship_to_fc.gstin, 2)[0]+')')
                    ws.write(row, 13, '')
                    ws.write(row, 14, '')
                    ws.write(row, 15, sts.ship_to_fc.code)
                    ws.write(row, 16, sts.ship_to_fc.city)
                    ws.write(row, 17, sts.ship_to_fc.state_id.name)
                    ws.write(row, 18, sts.ship_to_fc.country_id.name)
                    ws.write(row, 19, sts.ship_to_fc.pincode)
                    ws.write(row, 20, '')
                    ws.write(row, 21, '')
                    ws.write(row, 22, '')
                    ws.write(row, 23, sts_l.taxable_value)
                    ws.write(row, 24, sts_l.sales_ladgers)
                    ws.write(row, 25, '')
                    ws.write(row, 26, '')
                    ws.write(row, 27, '')
                    ws.write(row, 28, '')
                    ws.write(row, 29, sts_l.igst_amount)
                    ws.write(row, 30, 'Output Tax -IGST@ '+str(int(sts_l.igst_rate))+'%')
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
                    ws.write(row, 42, sts.ship_from_fc.code)
                    ws.write(row, 43, sts.invoice_date.strftime("%d-%m-%Y"))
                    ws.write(row, 44, str(sts.ord_id)+' '+str(sts.ship_to_fc.code)+' '+str(sts.ship_to_fc.city)+' '+str(sts.ship_to_fc.state_id.name)+' '+str(sts.ship_to_fc  .country_id.name)+' '+str(sts.ship_to_fc.pincode))
                    ws.write(row, 45, 'New Entity')
                    ws.write(row, 46, 'Br. Sale')
                    ws.write(row, 47, '')
                    ws.write(row, 48, sts.invoice_date.strftime("%d-%m-%Y"))
                    ws.write(row, 49, sts.name)
                    ws.write(row, 50, sts.name)
                    ws.write(row, 51, sts.ord_id)
                    ws.write(row, 52, sts_l.l10n_in_hsn_code.zfill(9))
                    ws.write(row, 53, '')
                    ws.write(row, 54, '')
                    ws.write(row, 55, sts.ship_from_fc.gstin)
                    ws.write(row, 56, sts.ship_to_fc.gstin)
                    ws.write(row, 57, sts.ship_from_fc.state_id.name)
                    ws.write(row, 58, sts_l.asin)
                    ws.write(row, 59, sts.trn_type)
                    row+=1    
        else:
            raise Warning("Currently No Stock Transfer Sale For This Data!!")
        filename = '/tmp/Stock_Transfer_Sale'+'.xls'
        workbook.save(filename)
        file = open(filename, "rb")
        file_data = file.read()
        out = base64.encodestring(file_data)
        self.write({'file_name': filename, 'file_xls':out, 'flag': True})
        return {
           'type': 'ir.actions.act_window',
           'res_model': 'stock.transfer.sale.xls',
           'view_mode': 'form',
           'view_type': 'form',
           'res_id': self.id,
           'target': 'new',
        }
class StockTranferPurchaseXls(models.TransientModel):
    _name = "stock.transfer.purchase.xls"
    _description = 'Stock Tranfer Purchase Xls'
    month_of_stock_trns = fields.Selection([
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
        ], string="Month of Stock Tranfer", required=True)
    ship_to_fc = fields.Many2one('stock.warehouse', string="Ship To Fc")
    file_name = fields.Char('Name', size=256)
    file_xls = fields.Binary(' Report', readonly=True)
    flag = fields.Boolean(string="Flag")

    def action_stock_tranfer_purchase_xls(self):
        print("============action_stock_tranfer_purchase_xls================")
        workbook = xlwt.Workbook()
        ws = workbook.add_sheet('Sheet1')
        s_h = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center")
        print("---------------------------------writting into sheet--------------------")
        ws.write(0, 0, 'Date', s_h)
        ws.write(0, 1, 'Purchase Order Number', s_h)
        ws.write(0, 2, 'Invoice number', s_h)
        ws.write(0, 3, 'Channel entry', s_h)
        ws.write(0, 4, 'Channel Ledger', s_h)
        ws.write(0, 5, 'Product Name', s_h)
        ws.write(0, 6, 'Product SKU Code', s_h)
        ws.write(0, 7, 'Qty', s_h)
        ws.write(0, 8, 'Unit Price', s_h)
        ws.write(0, 9, 'Currency', s_h)
        ws.write(0, 10, 'conversion rate', s_h)
        ws.write(0, 11, 'Total', s_h)
        ws.write(0, 12, 'Vendor Name', s_h)
        ws.write(0, 13, 'Shipping Address Name', s_h)
        ws.write(0, 14, 'Shipping Address Line 1', s_h)
        ws.write(0, 15, 'Shipping Address Line 2', s_h)
        ws.write(0, 16, 'Shipping Address City', s_h)
        ws.write(0, 17, 'Shipping Address State', s_h)
        ws.write(0, 18, 'Country', s_h)
        ws.write(0, 19, 'Shipping Address Pincode', s_h)
        ws.write(0, 20, 'Shipping Address Phone', s_h)
        ws.write(0, 21, 'Shipping Provider', s_h)
        ws.write(0, 22, 'AWB num', s_h)
        ws.write(0, 23, 'Purchase', s_h)
        ws.write(0, 24, 'Purchase Ledger', s_h)
        ws.write(0, 25, 'CGST', s_h)
        ws.write(0, 26, 'CGST Rate.', s_h)
        ws.write(0, 27, 'SGST', s_h)
        ws.write(0, 28, 'SGST Rate.', s_h)
        ws.write(0, 29, 'IGST', s_h)
        ws.write(0, 30, 'IGST Rate.', s_h)
        ws.write(0, 31, 'UTGST', s_h)
        ws.write(0, 32, 'UTGST Rate.', s_h)
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
        ws.write(0, 52, 'HSN Code', s_h)
        ws.write(0, 53, 'Units', s_h)
        ws.write(0, 54, 'Category', s_h)
        ws.write(0, 55, 'GST of Supplier', s_h)
        ws.write(0, 56, 'GST of Buyer', s_h)
        ws.write(0, 57, 'State of Receiver', s_h)
        ws.write(0, 58, 'Product ASIN', s_h)
        ws.write(0, 58, 'Transaction Type', s_h)
        stock_t_purchase_ids = None
        if self.month_of_stock_trns == 'all_month':
            if not self.ship_to_fc:
                print("---------------------1-------------") 
                stock_t_purchase_ids = self.env['stock.transfer.purchase'].search([], order='id asc')
        if self.month_of_stock_trns != 'all_month':
            if not self.ship_to_fc:
                print("---------------------2-------------") 
                stock_t_purchase_ids = self.env['stock.transfer.purchase'].search([('month_of_stock_trns', '=', self.month_of_stock_trns)], order='id asc')
        if self.month_of_stock_trns == 'all_month':
            if self.ship_to_fc:
                print("---------------------3-------------") 
                stock_t_purchase_ids = self.env['stock.transfer.purchase'].search([('ship_to_fc', '=', self.ship_to_fc.id)], order='id asc')
        if self.month_of_stock_trns != 'all_month':
            if self.ship_to_fc:
                print("---------------------4-------------") 
                stock_t_purchase_ids = self.env['stock.transfer.purchase'].search([('month_of_stock_trns', '=', self.month_of_stock_trns), ('ship_to_fc', '=', self.ship_to_fc.id)], order='id asc')
        if stock_t_purchase_ids:
            row = 1
            for stp in stock_t_purchase_ids:
                for stp_l in stp.stock_transfer_line:
                    ws.write(row, 0, stp.invoice_date.strftime("%d-%m-%Y"))
                    ws.write(row, 1, stp.sale_invoice)
                    ws.write(row, 2, stp.sale_invoice)
                    ws.write(row, 3, 'Br.Sinew Nutrition Private Ltd ('+wrap(stp.ship_to_fc.gstin, 2)[0]+'+'+wrap(stp.ship_from_fc.gstin, 2)[0]+')')
                    ws.write(row, 4, 'Br.Sinew Nutrition Private Ltd ('+wrap(stp.ship_to_fc.gstin, 2)[0]+'+'+wrap(stp.ship_from_fc.gstin, 2)[0]+')')
                    ws.write(row, 5, stp_l.product_product_id.name)
                    ws.write(row, 6, stp_l.default_code)
                    ws.write(row, 7, stp_l.quntity)
                    ws.write(row, 8, stp_l.unit_price)
                    ws.write(row, 9, '')
                    ws.write(row, 10, '')
                    ws.write(row, 11, stp_l.invoice_vales)
                    ws.write(row, 12, 'Br.Sinew Nutrition Private Ltd ('+wrap(stp.ship_to_fc.gstin, 2)[0]+'+'+wrap(stp.ship_from_fc.gstin, 2)[0]+')')
                    ws.write(row, 13, '')
                    ws.write(row, 14, '')
                    ws.write(row, 15, stp.ship_from_fc.code)
                    ws.write(row, 16, stp.ship_from_fc.city)
                    ws.write(row, 17, stp.ship_from_fc.state_id.name)
                    ws.write(row, 18, stp.ship_from_fc.country_id.name)
                    ws.write(row, 19, stp.ship_from_fc.pincode)
                    ws.write(row, 20, '')
                    ws.write(row, 21, '')
                    ws.write(row, 22, '')
                    ws.write(row, 23, stp_l.taxable_value)
                    ws.write(row, 24, stp_l.purchase_ladgers)
                    ws.write(row, 25, '')
                    ws.write(row, 26, '')
                    ws.write(row, 27, '')
                    ws.write(row, 28, '')
                    ws.write(row, 29, stp_l.igst_amount)
                    ws.write(row, 30, 'Output Tax -IGST@ '+str(int(stp_l.igst_rate))+'%') 
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
                    ws.write(row, 42, stp.ship_to_fc.code)
                    ws.write(row, 43, stp.invoice_date.strftime("%d-%m-%Y"))
                    ws.write(row, 44, str(stp.ord_id)+' '+str(stp.ship_from_fc.code)+' '+str(stp.ship_from_fc.city)+' '+str(stp.ship_from_fc.state_id.name)+' '+str(stp.ship_from_fc  .country_id.name)+' '+str(stp.ship_from_fc.pincode))
                    ws.write(row, 45, 'New Entity')
                    ws.write(row, 46, 'Br. Purchase')
                    ws.write(row, 47, '')
                    ws.write(row, 48, stp.invoice_date.strftime("%d-%m-%Y"))
                    ws.write(row, 49, stp.sale_invoice)
                    ws.write(row, 50, stp.sale_invoice)
                    ws.write(row, 51, stp.ord_id)
                    ws.write(row, 52, stp_l.l10n_in_hsn_code.zfill(9))
                    ws.write(row, 53, '')
                    ws.write(row, 54, '')
                    ws.write(row, 55, stp.ship_from_fc.gstin)
                    ws.write(row, 56, stp.ship_to_fc.gstin)
                    ws.write(row, 57, stp.ship_to_fc.state_id.name)
                    ws.write(row, 58, stp_l.asin)
                    ws.write(row, 59, stp.trn_type)
                    row+=1    
        else:
            raise Warning("Currently No Stock Transfer Purchase For This Data!!")
        filename = '/tmp/Stock_Transfer_Purchase'+ '.xls'
        workbook.save(filename)
        file = open(filename, "rb")
        file_data = file.read()
        out = base64.encodestring(file_data)
        self.write({'file_name': filename, 'file_xls':out, 'flag': True})
        return {
           'type': 'ir.actions.act_window',
           'res_model': 'stock.transfer.purchase.xls',
           'view_mode': 'form',
           'view_type': 'form',
           'res_id': self.id,
           'target': 'new',
        }