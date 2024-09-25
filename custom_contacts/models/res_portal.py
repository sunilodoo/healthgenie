# -*- coding: utf-8 -*-
import logging
from collections import namedtuple

from odoo import _, _lt, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ResPortal(models.Model):
	_name = 'res.portal'
	_description = 'Res Portal'
	# _order = 'sequence'
	# _order = "name desc"

	name = fields.Char(string="Portal Name", required=True)
	_sql_constraints = [
        ('name_name_uniq', 'unique(name)', 'The Portal Name must be unique')
    ]