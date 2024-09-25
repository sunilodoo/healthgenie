from odoo import models, api, fields, _



# url = "http://192.168.1.45:8069"
# db = "sinew_fy2223"
# username = "admin"
# password = "@gk!S^)!_0403@%2023"


class ReturnOrder(models.Model):
    _inherit = "return.order"

    def _action_confirm_return_order(self):
        print('-------NEW------')
        if self.state == 'draft':
            self._compute_invoice_amount()
            if self.name == 'New':
                if self.order_category == 'b2c':
                    self.name = '2324RT/' + str(self.warehouse_id.code) + '/' + str(self.warehouse_id.rto_b2c).zfill(4)
                    print('----------name-', self.name)
                    if self.name:
                        wh_so = self.warehouse_id.write({'rto_b2c': self.warehouse_id.rto_b2c + 1})
                        print('----------wh-so-', wh_so)
                if self.order_category == 'b2b':
                    self.name = '2324CN/' + str(self.warehouse_id.code) + '/' + str(self.warehouse_id.rto_b2b).zfill(4)
                    print('----------name-', self.name)
                    if self.sale_number_b2b:
                        wh_so = self.warehouse_id.write({'rto_b2b': self.warehouse_id.rto_b2b + 1})
                        print('----------wh-so-', wh_so)
            self.state = 'done'
            print("--------COMPLETE--------")

    def _compute_invoice_amount(self):
        print('---COMPUTE NEW METHOD---')
        for line in self:
            print("-----------------line-------", line)
            if line.invoice_line_id:
                line.product_product_id = line.invoice_line_id.product_id.id
                line.sale_order_id = line.invoice_line_id.move_id.so_id.id
                line.invoice_order_id = line.invoice_line_id.move_id.id
                line.odoo_order_b2b = line.invoice_line_id.move_id.invoice_number_b2b
                line.odoo_order_b2c = line.invoice_line_id.move_id.invoice_number
                line.from_warehouse_id = line.invoice_line_id.move_id.warehouse_id.id

                line.partner_name = line.invoice_line_id.move_id.partner_id.id
                line.partner_city = line.invoice_line_id.move_id.partner_id.city
                line.state_id = line.invoice_line_id.move_id.partner_id.state_id.id
                line.country_id = line.invoice_line_id.move_id.partner_id.country_id.id
                line.partner_zip_code = line.invoice_line_id.move_id.partner_id.zip
                line.partner_vat = line.invoice_line_id.move_id.partner_id.vat
                line.order_category = line.invoice_line_id.move_id.order_category
                line.sale_number_b2b = line.invoice_line_id.move_id.sale_number_b2b
                line.sale_number = line.invoice_line_id.move_id.sale_number
                line.tax_ids = line.invoice_line_id.tax_ids
                line.price_unit = line.invoice_line_id.price_unit
                line.product_hsn = line.invoice_line_id.product_hsn
                line.portal_price = line.invoice_line_id.portal_price
                line.shipping_charges = line.invoice_line_id.shipping_charges
                line.gift_wrap_price = line.invoice_line_id.gift_wrap_price
                line.item_promo_discount = line.invoice_line_id.item_promo_discount
            if line.portal_order_id and line.default_code:
                if not line.invoice_line_id:
                    line.original_order(line.portal_order_id, line.default_code)
            for tax in line.tax_ids:
                if line.invoice_order_id:
                    if line.invoice_order_id.order_category == 'b2b':
                        p_gstin = line.invoice_order_id.partner_id.vat
                        w_gstin = line.invoice_order_id.warehouse_id.gstin
                        p_gstin_s_c = p_gstin[0] + p_gstin[1]
                        w_gstin_s_c = w_gstin[0] + w_gstin[1]
                        if p_gstin_s_c == w_gstin_s_c:
                            tax_rate = tax.children_tax_ids[0].amount
                            tax_percentage = 2 * tax_rate
                            tax_amount = round((tax_percentage * line.portal_price / (100 + tax_percentage)) / 2, 2)
                            tax_amount_total = tax_amount * line.quntity
                            price_unit = line.portal_price - 2 * tax_amount
                            price_subtotal = price_unit * line.quntity
                            shipping_tax = 0.0
                            shipping_charges_basic = 0.0
                            if line.shipping_charges > 0:
                                shipping_tax = round(
                                    (line.shipping_charges * tax_percentage / (100 + tax_percentage)) / 2, 2)
                                shipping_charges_basic = line.shipping_charges - 2 * shipping_tax
                            gift_tax = 0.0
                            gift_wrap_basic = 0.0
                            if line.gift_wrap_price > 0:
                                gift_tax = round((line.gift_wrap_price * tax_percentage / (100 + tax_percentage)) / 2,
                                                 2)
                                gift_wrap_basic = line.gift_wrap_price - 2 * gift_tax
                            promo_tax = 0.0
                            item_promo_discount_basic = 0.0
                            if line.item_promo_discount > 0:
                                promo_tax = round(
                                    (line.item_promo_discount * tax_percentage / (100 + tax_percentage)) / 2, 2)
                                item_promo_discount_basic = line.item_promo_discount - 2 * promo_tax

                            line.update({
                                'price_unit': price_unit,
                                'price_subtotal': price_subtotal,
                                'price_tax': 2 * tax_amount_total,
                                'sgst_rate': tax.children_tax_ids[0].name,
                                'sgst_amount': tax_amount_total,
                                'cgst_rate': tax.children_tax_ids[1].name,
                                'cgst_amount': tax_amount_total,
                                'igst_rate': '',
                                'igst_amount': 0.0,
                                'tax_sum': tax_percentage,
                                'subtotal_with_tax': line.portal_price * line.quntity,

                                'shipping_charges_basic': shipping_charges_basic,
                                'shipping_charges_sgst': shipping_tax,
                                'shipping_charges_cgst': shipping_tax,
                                'shipping_charges_igst': 0.0,

                                'gift_wrap_basic': gift_wrap_basic,
                                'gift_wrap_sgst': gift_tax,
                                'gift_wrap_cgst': gift_tax,
                                'gift_wrap_igst': 0.0,

                                'item_promo_discount_basic': item_promo_discount_basic,
                                'item_promo_sgst': promo_tax,
                                'item_promo_cgst': promo_tax,
                                'item_promo_igst': 0.0,

                                'grand_subtotal': line.portal_price * line.quntity + line.shipping_charges + line.gift_wrap_price - line.item_promo_discount
                            })
                        else:
                            tax_rate = tax.children_tax_ids[0].amount
                            tax_percentage = 2 * tax_rate
                            tax_amount = round(tax_percentage * line.portal_price / (100 + tax_percentage), 2)
                            tax_amount_total = tax_amount * line.quntity
                            price_unit = line.portal_price - tax_amount
                            price_subtotal = price_unit * line.quntity

                            shipping_tax = 0.0
                            shipping_charges_basic = 0.0
                            if line.shipping_charges > 0:
                                shipping_tax = round(line.shipping_charges * tax_percentage / (100 + tax_percentage), 2)
                                shipping_charges_basic = line.shipping_charges - shipping_tax

                            gift_tax = 0.0
                            gift_wrap_basic = 0.0
                            if line.gift_wrap_price > 0:
                                gift_tax = round(line.gift_wrap_price * tax_percentage / (100 + tax_percentage), 2)
                                gift_wrap_basic = line.gift_wrap_price - gift_tax

                            promo_tax = 0.0
                            item_promo_discount_basic = 0.0
                            if line.item_promo_discount > 0:
                                promo_tax = round(line.item_promo_discount * tax_percentage / (100 + tax_percentage), 2)
                                item_promo_discount_basic = line.item_promo_discount - promo_tax

                            line.update({
                                'price_unit': line.portal_price - tax_amount,
                                'price_subtotal': price_subtotal,
                                'price_tax': tax_amount_total,
                                'sgst_rate': '',
                                'sgst_amount': 0.0,
                                'cgst_rate': '',
                                'cgst_amount': 0.0,
                                'igst_rate': 'IGST' + str(tax_percentage) + '%',
                                # 'igst_rate': 'IGST'+str(2*float(tax.children_tax_ids[0].amount))+'%',
                                'igst_amount': tax_amount_total,
                                'tax_sum': tax_percentage,
                                'subtotal_with_tax': line.portal_price * line.quntity,

                                'shipping_charges_basic': shipping_charges_basic,
                                'shipping_charges_sgst': 0.0,
                                'shipping_charges_cgst': 0.0,
                                'shipping_charges_igst': shipping_tax,

                                'gift_wrap_basic': gift_wrap_basic,
                                'gift_wrap_sgst': 0.0,
                                'gift_wrap_cgst': 0.0,
                                'gift_wrap_igst': gift_tax,

                                'item_promo_discount_basic': item_promo_discount_basic,
                                'item_promo_sgst': 0.0,
                                'item_promo_cgst': 0.0,
                                'item_promo_igst': promo_tax,

                                'grand_subtotal': line.portal_price * line.quntity + line.shipping_charges + line.gift_wrap_price - line.item_promo_discount
                            })
                    else:
                        if line.invoice_order_id.partner_id.state_id.name == line.invoice_order_id.warehouse_id.state_id.name:
                            tax_rate = tax.children_tax_ids[0].amount
                            tax_percentage = 2 * tax_rate
                            tax_amount = round((tax_percentage * line.portal_price / (100 + tax_percentage)) / 2, 2)
                            tax_amount_total = tax_amount * line.quntity
                            price_unit = line.portal_price - 2 * tax_amount
                            price_subtotal = price_unit * line.quntity
                            shipping_tax = 0.0
                            shipping_charges_basic = 0.0
                            if line.shipping_charges > 0:
                                shipping_tax = round(
                                    (line.shipping_charges * tax_percentage / (100 + tax_percentage)) / 2, 2)
                                shipping_charges_basic = line.shipping_charges - 2 * shipping_tax
                            gift_tax = 0.0
                            gift_wrap_basic = 0.0
                            if line.gift_wrap_price > 0:
                                gift_tax = round((line.gift_wrap_price * tax_percentage / (100 + tax_percentage)) / 2,
                                                 2)
                                gift_wrap_basic = line.gift_wrap_price - 2 * gift_tax
                            promo_tax = 0.0
                            item_promo_discount_basic = 0.0
                            if line.item_promo_discount > 0:
                                promo_tax = round(
                                    (line.item_promo_discount * tax_percentage / (100 + tax_percentage)) / 2, 2)
                                item_promo_discount_basic = line.item_promo_discount - 2 * promo_tax

                            line.update({
                                'price_unit': price_unit,
                                'price_subtotal': price_subtotal,
                                'price_tax': 2 * tax_amount_total,
                                'sgst_rate': tax.children_tax_ids[0].name,
                                'sgst_amount': tax_amount_total,
                                'cgst_rate': tax.children_tax_ids[1].name,
                                'cgst_amount': tax_amount_total,
                                'igst_rate': '',
                                'igst_amount': 0.0,
                                'tax_sum': tax_percentage,
                                'subtotal_with_tax': line.portal_price * line.quntity,

                                'shipping_charges_basic': shipping_charges_basic,
                                'shipping_charges_sgst': shipping_tax,
                                'shipping_charges_cgst': shipping_tax,
                                'shipping_charges_igst': 0.0,

                                'gift_wrap_basic': gift_wrap_basic,
                                'gift_wrap_sgst': gift_tax,
                                'gift_wrap_cgst': gift_tax,
                                'gift_wrap_igst': 0.0,

                                'item_promo_discount_basic': item_promo_discount_basic,
                                'item_promo_sgst': promo_tax,
                                'item_promo_cgst': promo_tax,
                                'item_promo_igst': 0.0,

                                'grand_subtotal': line.portal_price * line.quntity + line.shipping_charges + line.gift_wrap_price - line.item_promo_discount
                            
                            })
                        else:
                            tax_rate = tax.children_tax_ids[0].amount
                            tax_percentage = 2 * tax_rate
                            tax_amount = round(tax_percentage * line.portal_price / (100 + tax_percentage), 2)
                            tax_amount_total = tax_amount * line.quntity
                            price_unit = line.portal_price - tax_amount
                            price_subtotal = price_unit * line.quntity

                            shipping_tax = 0.0
                            shipping_charges_basic = 0.0
                            if line.shipping_charges > 0:
                                shipping_tax = round(line.shipping_charges * tax_percentage / (100 + tax_percentage), 2)
                                shipping_charges_basic = line.shipping_charges - shipping_tax

                            gift_tax = 0.0
                            gift_wrap_basic = 0.0
                            if line.gift_wrap_price > 0:
                                gift_tax = round(line.gift_wrap_price * tax_percentage / (100 + tax_percentage), 2)
                                gift_wrap_basic = line.gift_wrap_price - gift_tax

                            promo_tax = 0.0
                            item_promo_discount_basic = 0.0
                            if line.item_promo_discount > 0:
                                promo_tax = round(line.item_promo_discount * tax_percentage / (100 + tax_percentage), 2)
                                item_promo_discount_basic = line.item_promo_discount - promo_tax

                            line.update({
                                'price_unit': line.portal_price - tax_amount,
                                'price_subtotal': price_subtotal,
                                'price_tax': tax_amount_total,
                                'sgst_rate': '',
                                'sgst_amount': 0.0,
                                'cgst_rate': '',
                                'cgst_amount': 0.0,
                                'igst_rate': 'IGST' + str(tax_percentage) + '%',
                                # 'igst_rate': 'IGST'+str(2*float(tax.children_tax_ids[0].amount))+'%',
                                'igst_amount': tax_amount_total,
                                'tax_sum': tax_percentage,
                                'subtotal_with_tax': line.portal_price * line.quntity,

                                'shipping_charges_basic': shipping_charges_basic,
                                'shipping_charges_sgst': 0.0,
                                'shipping_charges_cgst': 0.0,
                                'shipping_charges_igst': shipping_tax,

                                'gift_wrap_basic': gift_wrap_basic,
                                'gift_wrap_sgst': 0.0,
                                'gift_wrap_cgst': 0.0,
                                'gift_wrap_igst': gift_tax,

                                'item_promo_discount_basic': item_promo_discount_basic,
                                'item_promo_sgst': 0.0,
                                'item_promo_cgst': 0.0,
                                'item_promo_igst': promo_tax,

                                'grand_subtotal': line.portal_price * line.quntity + line.shipping_charges + line.gift_wrap_price - line.item_promo_discount
                            })
                else:
                    if line.order_category == 'b2b':
                        p_gstin = line.partner_vat
                        w_gstin = line.from_warehouse_id.gstin
                        p_gstin_s_c = p_gstin[0] + p_gstin[1]
                        w_gstin_s_c = w_gstin[0] + w_gstin[1]
                        if p_gstin_s_c == w_gstin_s_c:
                            tax_rate = tax.children_tax_ids[0].amount
                            tax_percentage = 2 * tax_rate
                            tax_amount = round((tax_percentage * line.portal_price / (100 + tax_percentage)) / 2, 2)
                            tax_amount_total = tax_amount * line.quntity
                            price_unit = line.portal_price - 2 * tax_amount
                            price_subtotal = price_unit * line.quntity
                            shipping_tax = 0.0
                            shipping_charges_basic = 0.0
                            if line.shipping_charges > 0:
                                shipping_tax = round(
                                    (line.shipping_charges * tax_percentage / (100 + tax_percentage)) / 2, 2)
                                shipping_charges_basic = line.shipping_charges - 2 * shipping_tax
                            gift_tax = 0.0
                            gift_wrap_basic = 0.0
                            if line.gift_wrap_price > 0:
                                gift_tax = round((line.gift_wrap_price * tax_percentage / (100 + tax_percentage)) / 2,
                                                 2)
                                gift_wrap_basic = line.gift_wrap_price - 2 * gift_tax
                            promo_tax = 0.0
                            item_promo_discount_basic = 0.0
                            if line.item_promo_discount > 0:
                                promo_tax = round(
                                    (line.item_promo_discount * tax_percentage / (100 + tax_percentage)) / 2, 2)
                                item_promo_discount_basic = line.item_promo_discount - 2 * promo_tax

                            line.update({
                                'price_unit': price_unit,
                                'price_subtotal': price_subtotal,
                                'price_tax': 2 * tax_amount_total,
                                'sgst_rate': tax.children_tax_ids[0].name,
                                'sgst_amount': tax_amount_total,
                                'cgst_rate': tax.children_tax_ids[1].name,
                                'cgst_amount': tax_amount_total,
                                'igst_rate': '',
                                'igst_amount': 0.0,
                                'tax_sum': tax_percentage,
                                'subtotal_with_tax': line.portal_price * line.quntity,

                                'shipping_charges_basic': shipping_charges_basic,
                                'shipping_charges_sgst': shipping_tax,
                                'shipping_charges_cgst': shipping_tax,
                                'shipping_charges_igst': 0.0,

                                'gift_wrap_basic': gift_wrap_basic,
                                'gift_wrap_sgst': gift_tax,
                                'gift_wrap_cgst': gift_tax,
                                'gift_wrap_igst': 0.0,

                                'item_promo_discount_basic': item_promo_discount_basic,
                                'item_promo_sgst': promo_tax,
                                'item_promo_cgst': promo_tax,
                                'item_promo_igst': 0.0,

                                'grand_subtotal': line.portal_price * line.quntity + line.shipping_charges + line.gift_wrap_price - line.item_promo_discount
                            
                            })
                        else:
                            tax_rate = tax.children_tax_ids[0].amount
                            tax_percentage = 2 * tax_rate
                            tax_amount = round(tax_percentage * line.portal_price / (100 + tax_percentage), 2)
                            tax_amount_total = tax_amount * line.quntity
                            price_unit = line.portal_price - tax_amount
                            price_subtotal = price_unit * line.quntity

                            shipping_tax = 0.0
                            shipping_charges_basic = 0.0
                            if line.shipping_charges > 0:
                                shipping_tax = round(line.shipping_charges * tax_percentage / (100 + tax_percentage), 2)
                                shipping_charges_basic = line.shipping_charges - shipping_tax

                            gift_tax = 0.0
                            gift_wrap_basic = 0.0
                            if line.gift_wrap_price > 0:
                                gift_tax = round(line.gift_wrap_price * tax_percentage / (100 + tax_percentage), 2)
                                gift_wrap_basic = line.gift_wrap_price - gift_tax

                            promo_tax = 0.0
                            item_promo_discount_basic = 0.0
                            if line.item_promo_discount > 0:
                                promo_tax = round(line.item_promo_discount * tax_percentage / (100 + tax_percentage), 2)
                                item_promo_discount_basic = line.item_promo_discount - promo_tax

                            line.update({
                                'price_unit': line.portal_price - tax_amount,
                                'price_subtotal': price_subtotal,
                                'price_tax': tax_amount_total,
                                'sgst_rate': '',
                                'sgst_amount': 0.0,
                                'cgst_rate': '',
                                'cgst_amount': 0.0,
                                'igst_rate': 'IGST' + str(tax_percentage) + '%',
                                # 'igst_rate': 'IGST'+str(2*float(tax.children_tax_ids[0].amount))+'%',
                                'igst_amount': tax_amount_total,
                                'tax_sum': tax_percentage,
                                'subtotal_with_tax': line.portal_price * line.quntity,

                                'shipping_charges_basic': shipping_charges_basic,
                                'shipping_charges_sgst': 0.0,
                                'shipping_charges_cgst': 0.0,
                                'shipping_charges_igst': shipping_tax,

                                'gift_wrap_basic': gift_wrap_basic,
                                'gift_wrap_sgst': 0.0,
                                'gift_wrap_cgst': 0.0,
                                'gift_wrap_igst': gift_tax,

                                'item_promo_discount_basic': item_promo_discount_basic,
                                'item_promo_sgst': 0.0,
                                'item_promo_cgst': 0.0,
                                'item_promo_igst': promo_tax,

                                'grand_subtotal': line.portal_price * line.quntity + line.shipping_charges + line.gift_wrap_price - line.item_promo_discount
                            })
                    else:
                        if line.state_id.id == line.from_warehouse_id.state_id.id:
                            tax_rate = tax.children_tax_ids[0].amount
                            tax_percentage = 2 * tax_rate
                            tax_amount = round((tax_percentage * line.portal_price / (100 + tax_percentage)) / 2, 2)
                            tax_amount_total = tax_amount * line.quntity
                            price_unit = line.portal_price - 2 * tax_amount
                            price_subtotal = price_unit * line.quntity
                            shipping_tax = 0.0
                            shipping_charges_basic = 0.0
                            if line.shipping_charges > 0:
                                shipping_tax = round(
                                    (line.shipping_charges * tax_percentage / (100 + tax_percentage)) / 2, 2)
                                shipping_charges_basic = line.shipping_charges - 2 * shipping_tax
                            gift_tax = 0.0
                            gift_wrap_basic = 0.0
                            if line.gift_wrap_price > 0:
                                gift_tax = round((line.gift_wrap_price * tax_percentage / (100 + tax_percentage)) / 2,
                                                 2)
                                gift_wrap_basic = line.gift_wrap_price - 2 * gift_tax
                            promo_tax = 0.0
                            item_promo_discount_basic = 0.0
                            if line.item_promo_discount > 0:
                                promo_tax = round(
                                    (line.item_promo_discount * tax_percentage / (100 + tax_percentage)) / 2, 2)
                                item_promo_discount_basic = line.item_promo_discount - 2 * promo_tax

                            line.update({
                                'price_unit': price_unit,
                                'price_subtotal': price_subtotal,
                                'price_tax': 2 * tax_amount_total,
                                'sgst_rate': tax.children_tax_ids[0].name,
                                'sgst_amount': tax_amount_total,
                                'cgst_rate': tax.children_tax_ids[1].name,
                                'cgst_amount': tax_amount_total,
                                'igst_rate': '',
                                'igst_amount': 0.0,
                                'tax_sum': tax_percentage,
                                'subtotal_with_tax': line.portal_price * line.quntity,

                                'shipping_charges_basic': shipping_charges_basic,
                                'shipping_charges_sgst': shipping_tax,
                                'shipping_charges_cgst': shipping_tax,
                                'shipping_charges_igst': 0.0,

                                'gift_wrap_basic': gift_wrap_basic,
                                'gift_wrap_sgst': gift_tax,
                                'gift_wrap_cgst': gift_tax,
                                'gift_wrap_igst': 0.0,

                                'item_promo_discount_basic': item_promo_discount_basic,
                                'item_promo_sgst': promo_tax,
                                'item_promo_cgst': promo_tax,
                                'item_promo_igst': 0.0,

                                'grand_subtotal': line.portal_price * line.quntity + line.shipping_charges + line.gift_wrap_price - line.item_promo_discount
                            })
                        else:
                            tax_rate = tax.children_tax_ids[0].amount
                            tax_percentage = 2 * tax_rate
                            tax_amount = round(tax_percentage * line.portal_price / (100 + tax_percentage), 2)
                            tax_amount_total = tax_amount * line.quntity
                            price_unit = line.portal_price - tax_amount
                            price_subtotal = price_unit * line.quntity

                            shipping_tax = 0.0
                            shipping_charges_basic = 0.0
                            if line.shipping_charges > 0:
                                shipping_tax = round(line.shipping_charges * tax_percentage / (100 + tax_percentage), 2)
                                shipping_charges_basic = line.shipping_charges - shipping_tax

                            gift_tax = 0.0
                            gift_wrap_basic = 0.0
                            if line.gift_wrap_price > 0:
                                gift_tax = round(line.gift_wrap_price * tax_percentage / (100 + tax_percentage), 2)
                                gift_wrap_basic = line.gift_wrap_price - gift_tax

                            promo_tax = 0.0
                            item_promo_discount_basic = 0.0
                            if line.item_promo_discount > 0:
                                promo_tax = round(line.item_promo_discount * tax_percentage / (100 + tax_percentage), 2)
                                item_promo_discount_basic = line.item_promo_discount - promo_tax

                            line.update({
                                'price_unit': line.portal_price - tax_amount,
                                'price_subtotal': price_subtotal,
                                'price_tax': tax_amount_total,
                                'sgst_rate': '',
                                'sgst_amount': 0.0,
                                'cgst_rate': '',
                                'cgst_amount': 0.0,
                                'igst_rate': 'IGST' + str(tax_percentage) + '%',
                                # 'igst_rate': 'IGST'+str(2*float(tax.children_tax_ids[0].amount))+'%',
                                'igst_amount': tax_amount_total,
                                'tax_sum': tax_percentage,
                                'subtotal_with_tax': line.portal_price * line.quntity,

                                'shipping_charges_basic': shipping_charges_basic,
                                'shipping_charges_sgst': 0.0,
                                'shipping_charges_cgst': 0.0,
                                'shipping_charges_igst': shipping_tax,

                                'gift_wrap_basic': gift_wrap_basic,
                                'gift_wrap_sgst': 0.0,
                                'gift_wrap_cgst': 0.0,
                                'gift_wrap_igst': gift_tax,

                                'item_promo_discount_basic': item_promo_discount_basic,
                                'item_promo_sgst': 0.0,
                                'item_promo_cgst': 0.0,
                                'item_promo_igst': promo_tax,

                                'grand_subtotal': line.portal_price * line.quntity + line.shipping_charges + line.gift_wrap_price - line.item_promo_discount
                            })