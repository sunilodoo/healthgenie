# -*- coding: utf-8 -*-
import xlwt
import time
import base64
import calendar
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    def create_invoices(self):
        # sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        sale_orders = self.env['sale.order'].browse(sorted(self._context.get('active_ids', [])))
        print("--------------#-@@@@@sale_orders---------", sale_orders)  
        if self.advance_payment_method == 'delivered':
            sale_orders._create_invoices(final=self.deduct_down_payments)
        else:
            # Create deposit product if necessary
            if not self.product_id:
                vals = self._prepare_deposit_product()
                self.product_id = self.env['product.product'].create(vals)
                self.env['ir.config_parameter'].sudo().set_param('sale.default_deposit_product_id', self.product_id.id)

            sale_line_obj = self.env['sale.order.line']
            for order in sale_orders:
                amount, name = self._get_advance_details(order)

                if self.product_id.invoice_policy != 'order':
                    raise UserError(_('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
                if self.product_id.type != 'service':
                    raise UserError(_("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
                taxes = self.product_id.taxes_id.filtered(lambda r: not order.company_id or r.company_id == order.company_id)
                tax_ids = order.fiscal_position_id.map_tax(taxes, self.product_id, order.partner_shipping_id).ids
                analytic_tag_ids = []
                for line in order.order_line:
                    analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]

                so_line_values = self._prepare_so_line(order, analytic_tag_ids, tax_ids, amount)
                so_line = sale_line_obj.create(so_line_values)
                self._create_invoice(order, so_line, amount)
        if self._context.get('open_invoices', False):
            return sale_orders.action_view_invoice()
        return {'type': 'ir.actions.act_window_close'}
    def action_create_invoice_so(self):
        # sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        # sale_orders = self.env['sale.order'].browse(sorted(self._context.get('active_ids', [])))
        sale_orders = self.env['sale.order'].search([('invoice_status', '=', 'to invoice')], order='id asc')
        print("---------------@@@@@sale_orders---------", sale_orders)
        print("--------------1------------", self.advance_payment_method)
        print("---------------len----", len(sale_orders))
        # for i in sale_orders:
        #     print("-------------i---", i.name)
        if self.advance_payment_method == 'delivered':
            sale_orders._create_invoices(final=self.deduct_down_payments)
        else:
            # Create deposit product if necessary
            if not self.product_id:
                vals = self._prepare_deposit_product()
                self.product_id = self.env['product.product'].create(vals)
                self.env['ir.config_parameter'].sudo().set_param('sale.default_deposit_product_id', self.product_id.id)

            sale_line_obj = self.env['sale.order.line']
            for order in sale_orders:
                amount, name = self._get_advance_details(order)

                if self.product_id.invoice_policy != 'order':
                    raise UserError(_('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
                if self.product_id.type != 'service':
                    raise UserError(_("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
                taxes = self.product_id.taxes_id.filtered(lambda r: not order.company_id or r.company_id == order.company_id)
                tax_ids = order.fiscal_position_id.map_tax(taxes, self.product_id, order.partner_shipping_id).ids
                analytic_tag_ids = []
                for line in order.order_line:
                    analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]

                so_line_values = self._prepare_so_line(order, analytic_tag_ids, tax_ids, amount)
                so_line = sale_line_obj.create(so_line_values)
                self._create_invoice(order, so_line, amount)
        if self._context.get('open_invoices', False):
            return sale_orders.action_view_invoice()
        return {'type': 'ir.actions.act_window_close'}

class B2BSaleOrderXlsReport(models.TransientModel):
    _name = "b2b.sale.order.report"
    _description = 'B2B Sale Order Xls Report'
    start_date = fields.Date(string='Date From', required=True)
    end_date = fields.Date(string='Date To', required=True)
    # start_date = fields.Date(string='Start Date', required=True, default=datetime.today().replace(day=1).date())
    # end_date = fields.Date(string="End Date", required=True, default=datetime.now().replace(day = calendar.monthrange(datetime.now().year, datetime.now().month)[1]).date())
    order_state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', default='draft', required=True)
    # user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user, required=True)
    file_name = fields.Char('Name', size=256)
    file_xls = fields.Binary(' Report', readonly=True)
    flag = fields.Boolean(string="Flag")
    # state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')

    _sql_constraints = [
            ('check','CHECK((start_date <= end_date))',"End date must be greater then start date")  
    ]

    # @api.multi
    def b2b_sale_order_xls(self):
        print("============aaction_b2b_sale_order_report================")
        file = StringIO()        
        sale_order = self.env['sale.order'].search([('date_order', '>=', self.start_date), ('date_order', '<=', self.end_date), ('state', '=', self.order_state)])
        print("--------------sale_order--------------------", sale_order)
        final_value = {}
        print("--------------final_value--------------------", final_value)
        workbook = xlwt.Workbook()                         
        """if sale_order:
            for rec in sale_order:
                order_lines = []
                for lines in rec.order_line:
                    product = {
                        'product_id'     : lines.product_id.item_code,
                        'description'    : lines.name,
                        'product_uom_qty': lines.product_uom_qty,
                        #'brand'  : lines.brand.name,
                        'unit'   : lines.product_uom.name,
                        'price_unit'     : lines.price_unit,
                        'price_subtotal' : lines.price_subtotal   
                    }
                    if lines.tax_id:
                        taxes = []
                        for tax_id in lines.tax_id:
                            taxes.append(tax_id.name)
                        product['tax_id'] = taxes
                    order_lines.append(product)
                final_value['partner_id'] = rec.partner_id.name
                final_value['street'] = rec.partner_id.street
                final_value['street2'] = rec.partner_id.street2
                final_value['city'] = rec.partner_id.city
                final_value['state'] = rec.partner_id.state_id.name
                final_value['country'] = rec.partner_id.country_id.name
                final_value['date_order'] = rec.date_order
                final_value['user_id'] = rec.user_id.name
                final_value['name'] = rec.name
                final_value['currency_id'] = rec.currency_id
                #final_value['state'] = dict(self.env['sale.order'].fields_get(allfields=['state'])['state']['selection'])[rec.state]
                # final_value['carrier_id'] = rec.carrier_id.name
                # final_value['dispatch'] = rec.date_to_dispatch.name
                # final_value['delivery'] = rec.deli_to.name
                final_value['buyerref'] = rec.buyer_ref
                final_value['buyerdate'] = rec.buyer_date
                final_value['payment_term_id'] = rec.payment_term_id.name
                final_value['incoterms'] = rec.incoterms.name
                final_value['origin'] = rec.origin
                final_value['amount_untaxed'] = rec.amount_untaxed
                final_value['amount_tax'] = rec.amount_tax
                final_value['amount_total'] = rec.amount_total
                # final_value['other_charge'] = rec.other_charge
                final_value['freight_charge'] = rec.freight_charge
                final_value['global_disc'] = rec.global_disc
                final_value['full_total'] = rec.full_total
                format0 = xlwt.easyxf('font:height 500,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
                format1 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
                format2 = xlwt.easyxf('font:bold True;align: horiz left')
                format3 = xlwt.easyxf('align: horiz left')
                format4 = xlwt.easyxf('align: horiz right')
                format5 = xlwt.easyxf('font:bold True;align: horiz right')
                format6 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz right')
                format7 = xlwt.easyxf('font:bold True;borders:top thick;align: horiz right')
                format8 = xlwt.easyxf('font:bold True;borders:top thick;pattern: pattern solid, fore_colour gray25;align: horiz left')
                sheet = workbook.add_sheet(rec.name)
                sheet.col(0).width = int(30*260)
                sheet.col(1).width = int(30*260)    
                sheet.col(2).width = int(18*260)    
                sheet.col(3).width = int(18*260) 
                sheet.col(4).width = int(15*260)   
                sheet.col(5).width = int(15*260)
                sheet.col(6).width = int(33*260)   
                sheet.write_merge(0, 2, 0, 7, 'Sale Order : ' + final_value['name'] , format0)
                sheet.write(5, 0, "Customer Informatrion", format1)
                sheet.write(5, 1, final_value['partner_id'], format2)
                sheet.write(6, 1, final_value['street'], format2)
                sheet.write(7, 1, final_value['street2'], format2)
                sheet.write(8, 1, final_value['city'], format2)
                sheet.write(9, 1, final_value['state'], format2)
                sheet.write(10, 1, final_value['country'], format2)
                sheet.write(5, 3, 'Date', format1)
                sheet.write_merge(5, 5, 4, 5, final_value['date_order'], format3)
                sheet.write(6, 3, 'Payment Term', format1)
                if final_value['payment_term_id']:
                    sheet.write_merge(6, 6, 4, 5, final_value['payment_term_id'], format3)
                else:
                    sheet.write_merge(6, 6, 4, 5, "No Payment Terms Defined", format3)

                sheet.write(7, 3, 'Incoterms', format1)
                if final_value['incoterms']:
                    sheet.write_merge(7, 7, 4, 5, final_value['incoterms'], format3)
                else:
                    sheet.write_merge(7, 7, 4, 5, "", format3)
                sheet.write(8, 3, "Delivery Method", format1)
                # sheet.write_merge(8, 8, 4, 5, final_value['carrier_id'], format3)

                sheet.write(9, 3, 'Days Of Dispatch', format1)
                if final_value['dispatch']:
                    sheet.write_merge(9, 9, 4, 5, final_value['dispatch'], format3)
                else:
                    sheet.write_merge(10, 10, 4, 5, "", format3)
                sheet.write(11, 3, "Delivery TO", format1)
                sheet.write_merge(11, 11, 4, 5, final_value['delivery'], format3)


                sheet.write(12, 3, 'Buyer Order No', format1)
                if final_value['buyerref']:
                    sheet.write_merge(12, 12, 4, 5, final_value['buyerref'], format3)
                else:
                    sheet.write_merge(13, 13, 4, 5, "", format3)
                sheet.write(13, 3, "Buyer Order Date", format1)
                sheet.write_merge(13, 13, 4, 5, final_value['buyerdate'], format3)


                sheet.write(12, 0, "Salesperson", format1)
                sheet.write(12, 1, final_value['user_id'], format3)
                sheet.write(15, 0, 'PRODUCT', format1)
                sheet.write_merge(15, 15,1,2, 'DESCRIPTION', format1)
                #sheet.write(15, 2, 'BRAND', format6)
                sheet.write(15, 3, 'QUANTITY', format6)                
                sheet.write(15, 4, 'UOM', format6)        
                sheet.write(15, 5, 'UNIT PRICE', format6)
                sheet.write(15, 6, 'TAXES', format1) 
                sheet.write(15, 7, 'SUBTOTAL', format6)
                row = 16
                for rec in order_lines:
                    sheet.write(row, 0, rec.get('product_id'), format3)
                    sheet.write_merge(row, row,1,2, rec.get('description'), format3)
                    #sheet.write(row, 2, rec.get('brand'), format4)
                    sheet.write(row, 3, rec.get('product_uom_qty'), format4)
                    sheet.write(row, 4, rec.get('unit'), format4)
                    sheet.write(row, 5, rec.get('price_unit'), format4)
                    if rec.get('tax_id'):
                        sheet.write(row, 6, ",".join(rec.get('tax_id')), format4)
                    else:
                        sheet.write(row, 6, 0, format4)
                    if final_value['currency_id'].position == "before":
                        sheet.write(row, 7, final_value['currency_id'].symbol + str(rec.get('price_subtotal')), format4)
                    else:
                        sheet.write(row, 7, str(rec.get('price_subtotal')) + final_value['currency_id'].symbol, format4)
                    row += 1
                row += 2
                sheet.write(row, 6, 'UNTAXED AMOUNT', format8)
                if final_value['currency_id'].position == "before":
                    sheet.write(row, 7, final_value['currency_id'].symbol + str(final_value['amount_untaxed']), format7)
                else:
                    sheet.write(row, 7, str(final_value['amount_untaxed']) + final_value['currency_id'].symbol, format7)    
                sheet.write(row+1, 6, 'TAXES', format8)


                if final_value['currency_id'].position == "before":
                    sheet.write(row+1, 7, final_value['currency_id'].symbol + str(final_value['amount_tax']), format7)
                else:
                    sheet.write(row+1, 7, str(final_value['amount_tax']) + final_value['currency_id'].symbol, format7)
                sheet.write(row+2, 6, 'TOTAL', format8)


                if final_value['currency_id'].position == "before":
                    sheet.write(row+2, 7, final_value['currency_id'].symbol + str(final_value['amount_total']), format7)
                else:
                    sheet.write(row+2, 7, str(final_value['amount_total']) + final_value['currency_id'].symbol, format7)

                sheet.write(row+3, 6, 'OTHER CHARGES', format8)
                if final_value['currency_id'].position == "before":
                    sheet.write(row+3, 7, final_value['currency_id'].symbol + str(final_value['other_charge']), format7)
                else:
                    sheet.write(row+3, 7, str(final_value['other_charge']) + final_value['currency_id'].symbol, format7)
                
                sheet.write(row+4, 6, 'FRIEGHT CHARGE', format8)
                if final_value['currency_id'].position == "before":
                    sheet.write(row+4, 7, final_value['currency_id'].symbol + str(final_value['freight_charge']), format7)
                else:
                    sheet.write(row+4, 7, str(final_value['freight_charge']) + final_value['currency_id'].symbol, format7)

                sheet.write(row+5, 6, 'DISCOUNT', format8)
                if final_value['currency_id'].position == "before":
                    sheet.write(row+5, 7, final_value['currency_id'].symbol + str(final_value['global_disc']), format7)
                else:
                    sheet.write(row+5, 7, str(final_value['global_disc']) + final_value['currency_id'].symbol, format7)
                
                sheet.write(row+6, 6, 'GRAND TOTAL', format8)
                if final_value['currency_id'].position == "before":
                    sheet.write(row+6, 7, final_value['currency_id'].symbol + str(final_value['full_total']), format7)
                else:
                    sheet.write(row+6, 7, str(final_value['full_total']) + final_value['currency_id'].symbol, format7)
        else:
            raise Warning("Currently No Sales Order For This Data!!")"""
        sheet = workbook.add_sheet('sales_report')
        filename = 'Sale Order Report'+ '.xls'
        workbook.save(filename)
        file = open(filename, "rb")
        file_data = file.read()
        out = base64.encodestring(file_data)
        self.write({'file_name': filename, 'file_xls':out, 'flag': True})
        return {
           'type': 'ir.actions.act_window',
           'res_model': 'b2b.sale.order.report',
           'view_mode': 'form',
           'view_type': 'form',
           'res_id': self.id,
           'target': 'new',
        }
class B2CSaleOrderXlsReport(models.TransientModel):
    _name = "b2c.sale.order.report"
    _description = 'B2B Sale Order Xls Report'
    start_date = fields.Date(string='Date From', required=True)
    end_date = fields.Date(string='Date To', required=True)
    order_state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', default='draft', required=True)
    file_name = fields.Char('Name', size=256)
    file_xls = fields.Binary(' Report', readonly=True)
    flag = fields.Boolean(string="Flag")
    def b2c_sale_order_xls(self):
        print("============action_b2c_report================")
        workbook = xlwt.Workbook()
        ws = workbook.add_sheet('sales_report')
        s_h = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center")
        print("---------------------------------writting into sheet--------------------")
        ws.write(0, 0, 'Order no', s_h)
        ws.write(0, 1, 'Invoice no', s_h)
        ws.write(0, 2, 'Invoice Date', s_h)
        ws.write(0, 3, 'Suborder id', s_h)
        ws.write(0, 4, 'Order date', s_h)
        ws.write(0, 5, 'Order status', s_h)
        ws.write(0, 6, 'Category', s_h)
        ws.write(0, 7, 'Brand', s_h)
        ws.write(0, 8, 'Sku', s_h)
        ws.write(0, 9, 'Item Name', s_h)
        ws.write(0, 10, 'Customer Name', s_h)
        ws.write(0, 11, 'Customer Shipping Address', s_h)
        ws.write(0, 12, 'Shipping State', s_h)
        ws.write(0, 13, 'Zip Code', s_h)
        ws.write(0, 14, 'Contact Number', s_h)
        ws.write(0, 15, 'Product Magento Id', s_h)
        ws.write(0, 16, 'Cost', s_h)
        ws.write(0, 17, 'Qty', s_h)
        ws.write(0, 18, 'Freight(Shipping Charges)', s_h)
        ws.write(0, 19, 'Unit Price Exc. Tax', s_h)
        ws.write(0, 20, 'Total Unit P. Exc Tax', s_h)
        ws.write(0, 21, 'Selling Price', s_h)
        ws.write(0, 22, 'Total Amount Inc. Tax', s_h)
        ws.write(0, 23, 'Tax Amount', s_h)
        ws.write(0, 24, 'City', s_h)
        ws.write(0, 25, 'Carrier', s_h)
        ws.write(0, 26, 'Weight', s_h)
        ws.write(0, 27, 'Payment from website', s_h)
        ws.write(0, 28, 'Frontend/backend', s_h)
        ws.write(0, 29, 'Mode of payment ', s_h)
        ws.write(0, 30, 'Tracking Ref', s_h)
        ws.write(0, 31, 'Shipped Date ', s_h)
        ws.write(0, 32, 'Delivery Date ', s_h)
        ws.write(0, 33, 'Product Internal Code', s_h)
        ws.write(0, 34, 'COD', s_h)
        ws.write(0, 35, 'Categ', s_h)
        ws.write(0, 36, 'Sub-categ', s_h)
        s_o_ids = self.env['sale.order'].search([('date_order', '>=', self.start_date), ('date_order', '<=', self.end_date), ('state', '=', self.order_state)])
        if s_o_ids:
            row = 1
            for so in s_o_ids:
                ws.write(row, 0, so.name)
            row+=1    
        else:
            raise Warning("Currently No Sales Order For This Data!!")


        filename = 'Sale Order Report'+ '.xls'
        workbook.save(filename)
        file = open(filename, "rb")
        file_data = file.read()
        out = base64.encodestring(file_data)
        self.write({'file_name': filename, 'file_xls':out, 'flag': True})
        return {
           'type': 'ir.actions.act_window',
           'res_model': 'b2c.sale.order.report',
           'view_mode': 'form',
           'view_type': 'form',
           'res_id': self.id,
           'target': 'new',
        }
