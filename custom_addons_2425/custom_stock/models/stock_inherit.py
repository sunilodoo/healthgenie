# -*- coding: utf-8 -*-
import logging
from collections import namedtuple

from odoo import _, _lt, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class WarehuseInherit(models.Model):
	_inherit = 'stock.warehouse'
	# _order = 'sequence'
	# _order = "name desc"

	# fs = fields.Char(string="FS")
	inv_code = fields.Char(string="Next Number(Invoice Code)", default=1)
	b2b_code = fields.Char(string="Next Number(B2B Code)", default=1)
	next_number_so_f = fields.Integer(string="Next Number(SO Fliipkart)", default=1)
	next_number_so_o = fields.Integer(string="Next Number(SO Others)", default=1)
	next_number_inv_f = fields.Integer(string="Next Number(Inv. Flipkart)", default=1)
	next_number_inv_o = fields.Integer(string="Next Number(Inv. Others)", default=1)
	stock_tranfer_code = fields.Char(string="Stock Tranfer Code")
	next_number_s_t_s = fields.Integer(string="Next Number Stock Tranfer Sale", default=1)
	next_number_s_t_p = fields.Integer(string="Next Number Stock Tranfer Purchase",  default=1)
	country_id = fields.Many2one(related='partner_id.country_id', string="Country", store=True)
	state_id = fields.Many2one(related='partner_id.state_id', string="State", domain="[('country_id', '=', country_id)]", store=True)
	rto_b2b = fields.Integer(string="RTO B2B",  default=1)
	rto_b2c = fields.Integer(string="RTO B2C",  default=1)
	# food_enabled = fields.Boolean(string="Food Enabled")
	hb_mps = fields.Selection([('hb', 'H&B'), ('mps', 'MPS')], string="H&B/MPS")
	# fc_into_gst = fields.Boolean(string="FC added into our GST")
	buiding = fields.Char(related='partner_id.street', string="Buiding", store=True)
	road = fields.Char(related='partner_id.street2',string="Road", store=True)
	city = fields.Char(related='partner_id.city',string="City", store=True)
	district = fields.Char(string="District")
	pincode = fields.Char(related='partner_id.zip',string="Pincode", store=True)
	tin = fields.Char(string="TIN")
	ownership = fields.Char(string="Ownership")
	gstin = fields.Char(related='partner_id.vat', string="GSTIN", store=True)
