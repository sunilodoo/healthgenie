# -*- coding: utf-8 -*-

from odoo import models, fields, osv, api, _
# from odoo.exceptions import Warning, UserError
from datetime import timedelta
# import datetime
# import logging
# import num2words

# _logger = logging.getLogger(__name__)

class SaleOrdermissing(models.Model):
	_name = "sale.order.missing"
	# _order = "date desc"
	_description = 'Sale Order Missing'
	channel_name = fields.Char(string="Channel Name")
	order_no = fields.Char(string="Order No")
	sku_name = fields.Char(string="SKU Name")
	pincode = fields.Char(string="Pin Code")