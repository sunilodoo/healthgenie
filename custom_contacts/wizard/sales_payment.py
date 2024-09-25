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
import xlwt
import base64
import datetime as dt
from odoo.exceptions import Warning, UserError
import logging

_logger = logging.getLogger(__name__)


class SalesPayment(models.TransientModel):
    _name = 'sales.payment'
    _description = 'Sales Payment'

    csv_file = fields.Binary(string='CSV File', required=True, help='File should be separated by comma (,) and quoted using Quote character (") ')
    # country_id = fields.Many2one('res.country', string="Country", required=True)
    # state_id = fields.Many2one('res.country.state', string="State", domain="[('country_id', '=', country_id)]")

    def import_payment(self):
        # pincode_pool = self.env['res.partner']
        # state_pool = self.env['res.country.state']
        # country_pool = self.env['res.country']
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
            order_id = row[headers['Order Id']].strip()
            # state = row[headers['State']].strip()
            # if not self.env['pincode.state'].search([('name', '=', pincode)]):
            payment_data = self.env['sale.order'].search([('order_id', '=', order_id)])
            print("f:::::::::::::::::::::::;",payment_data)
            for rec in payment_data:
                payment_vals = {}
                # print('rec::::::::::::::',rec.sale_payment_ids)
                # for s in rec.sale_payment_ids:
                #     print("ssssssssssssssss",s)
                payment_vals = { 
                                'comission': row[headers['Commission']].strip(),
                                'comission_cgst': row[headers['Commission CGST']].strip(),
                                'comission_igst': row[headers['Commission IGST']].strip(),
                                'comission_sgst': row[headers['Commission IGST']].strip(),
                                'current_reserve_ammount': row[headers['Current Reserve Amount']].strip(),
                                'fba_pick_and_pack': row[headers['FBA Pick and Pack Fee']].strip(),
                                'fba_pick_and_pack_cgst': row[headers['FBA Pick and Pack Fee CGST']].strip(),
                                'fba_pick_and_pack_sgst': row[headers['FBA Pick and Pack Fee SGST']].strip(),
                                'fba_weight_handling_fee': row[headers['FBA Weight Handling Fee']].strip(),
                                'fba_weight_handling_fee_cgst': row[headers['FBA Weight Handling Fee CGST']].strip(),
                                'fba_weight_handling_fee_sgst': row[headers['FBA Weight Handling Fee SGST']].strip(),
                                'fixed_closing_fees': row[headers['Fixed Closing Fees']].strip(),
                                'fixed_closing_fees_cgst': row[headers['Fixed Closing Fees CGST']].strip(),
                                'fixed_closing_fees_sgst': row[headers['Fixed Closing Fees SGST']].strip(),
                                'fixed_closing_fees_igst': row[headers['Fixed Closing Fees IGST']].strip(),
                                'gift_wrap': row[headers['Gift Wrap']].strip(),
                                'gift_wrap_charge_back': row[headers['Gift Wrap Charge Back']].strip(),
                                'gift_wrap_charge_cgst': row[headers['Gift Wrap Charge CGST']].strip(),
                                'gift_wrap_charge_sgst': row[headers['Gift Wrap Charge SGST']].strip(),
                                'gift_wrap_tax': row[headers['Gift Wrap Tax']].strip(),
                                'payment_retraction_item': row[headers['Payment Retraction Item']].strip(),
                                'principal': row[headers['Principal']].strip(),
                                'product_tax': row[headers['Product Tax']].strip(),
                                'product_tax_discount': row[headers['Product Tax Discount']].strip(),
                                'promo_rebates': row[headers['Promo Rebates']].strip(),
                                'refund_commission': row[headers['Refund Commission']].strip(),
                                'refund_commission_igst': row[headers['Refund Commission IGST']].strip(),
                                'removal_complete': row[headers['Removal Complete']].strip(),
                                'removal_complete_cgst': row[headers['Removal Complete CGST']].strip(),
                                'removal_complete_sgst': row[headers['Removal Complete SGST']].strip(),
                                'shipping': row[headers['Shipping']].strip(),
                                'shipping_charge_back': row[headers['Shipping Chargeback']].strip(),
                                'shipping_charge_back_cgst': row[headers['Shipping ChargeBack CGST']].strip(),
                                'shipping_charge_back_sgst': row[headers['Shipping ChargeBack SGST']].strip(),
                                'shipping_discount': row[headers['Shipping Discount']].strip(),
                                'shipping_tax': row[headers['Shipping Tax']].strip(),
                                'shipping_tax_discount': row[headers['Shipping Tax Discount']].strip(),
                                'storage_fee': row[headers['Storage Fee']].strip(),
                                'storage_billing_cgst': row[headers['Storage Billing CGST']].strip(),
                                'storage_billing_sgst': row[headers['Storage Billing SGST']].strip(),
                                'storage_reniew_billing': row[headers['Storage Renewal Billing']].strip(),
                                'storage_reniew_billing_cgst': row[headers['Storage Renewal Billing CGST']].strip(),
                                'storage_reniew_billing_sgst': row[headers['Storage Renewal Billing SGST']].strip(),
                                'tcs_cgst': row[headers['TCS-CGST']].strip(),
                                'tcs_igst': row[headers['TCS-IGST']].strip(),
                                'tcs_sgst': row[headers['TCS-SGST']].strip(),
                                'tds': row[headers['TDS (Section 194-O)']].strip(),
                                'technology_fee': row[headers['Technology Fee']].strip(),
                                'technology_fee_igst': row[headers['Technology Fee IGST']].strip(),
                               


                }
                print("----------payment_vals-------", payment_vals)
                ps = rec.write({'sale_payment_ids': [(0,0, payment_vals)]})
                print("ps::::::::::::::::;",ps)
        
        
            
            #         print("--------p_s--------------", p_s)
            #         count = count+1
            # # print("------------------------count---------------", count)



class SalesPaymentReport(models.TransientModel):
    _name = "sales.payment.report"
    _description = 'Xls Report'
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
        ], string="Month of sale", default=False)
    # start_date = fields.Date(string='Date From', required=True)
    # end_date = fields.Date(string='Date To', required=True)
    start_date = fields.Date(string='Date From')
    end_date = fields.Date(string='Date To')
    invoice_state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
        ], string='Status', default='posted', required=True)
    file_name = fields.Char('Name', size=256)
    file_xls = fields.Binary(' Report', readonly=True)
    flag = fields.Boolean(string="Flag")
    _sql_constraints = [
            ('check','CHECK((start_date <= end_date))',"End date must be greater then start date")  
    ]

    def sale_payment_report(self):
        # print("============action_report================")
        workbook = xlwt.Workbook()
        ws = workbook.add_sheet('Sheet1')
        s_h = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center")
        print("---------------------------------writting into sheet--------------------")
        ws.write(0, 0, 'Order Id', s_h)
        ws.write(0, 1, 'Sale Amount', s_h)
        ws.write(0, 2, 'Return Payment', s_h)
        ws.write(0, 3, 'Payment Recieved', s_h)
        ws.write(0, 4, 'Short & excess received', s_h)
       
        # invoice_ids = None
        if self.month_of_sale:
            # print("-----------self.month_of_sale:----", self.month_of_sale)
            sale_order_ids = self.env['sale.order'].search([('month_of_sale', '=', self.month_of_sale)], order='id asc')
            # print("-----------invoice_ids----", invoice_ids)
        # if self.start_date and self.end_date:
        #     invoice_ids = self.env['account.move'].search([('invoice_date', '>=', self.start_date), ('invoice_date', '<=', self.end_date), ('state', '=', self.invoice_state)], order='id asc')
        # # print("-------------invoice_ids--------------", invoice_ids)
        if sale_order_ids:
            row = 1
            for rec in sale_order_ids:
              
                
                ws.write(row, 0, rec.order_id)
                ws.write(row, 1, rec.amount_total)
                ws.write(row, 2, rec.return_payment)
                ws.write(row, 3, rec.payment_recieved)
                ws.write(row, 4, rec.short_access_recieved)
               
                
                row+=1    
        else:
            raise Warning("Currently No Payment For This Data!!")
        filename = '/tmp/Reports'+ '.xls'
        workbook.save(filename)
        file = open(filename, "rb")
        file_data = file.read()
        out = base64.encodebytes(file_data)
        self.write({'file_name': filename, 'file_xls':out, 'flag': True})
        return {
           'type': 'ir.actions.act_window',
           'res_model': 'sales.payment.report',
           'view_mode': 'form',
           'view_type': 'form',
           'res_id': self.id,
           'target': 'new',
        }
