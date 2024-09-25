# -*- coding: utf-8 -*-
import logging
from collections import namedtuple

from odoo import _, _lt, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class PincodeStatewise(models.Model):
	_name = 'pincode.state'
	_description = 'Pincode With State'
	# _order = 'sequence'
	# _order = "name desc"

	name = fields.Char(string="Pincode", required=True)
	district = fields.Char(string="District")
	country_id = fields.Many2one('res.country', string="Country", default=104, required=True)
	state_id = fields.Many2one('res.country.state', string="State", domain="[('country_id', '=', country_id)]", required=True)
	# state_id = fields.Many2one('res.country.state', string="State", domain="[('country_id','=','IT')]", domain="[('country_id', '=?', country_id)]"), domain="[('country_id', '=', country_id)]"
	_sql_constraints = [
        ('name_name_uniq', 'unique(name)', 'The Pincode of the state must be unique')
    ]