# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import Counter

from odoo import _, api, fields, tools, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import OrderedSet
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class StockMoveLine(models.Model):
	_inherit = "stock.move.line"
	_description = 'Stock Move Line'
	def _onchange_qty_done_inherit(self):
		# print("--------------------------_onchange_qty_done_inherit--------------")
		#When the user is encoding a move line for a tracked product, we apply some logic to	help him. This onchange will warn him if he set `qty_done` to a non-supported value.
		self.update({'qty_done': self.product_uom_qty})
		res = {}
		if self.qty_done and self.product_id.tracking == 'serial':
			qty_done = self.product_uom_id._compute_quantity(self.qty_done, self.product_id.uom_id)
			if float_compare(qty_done, 1.0, precision_rounding=self.product_id.uom_id.rounding) != 0:
				message = _('You can only process 1.0 %s of products with unique serial number.', self.product_id.uom_id.name)
				res['warning'] = {'title': _('Warning'), 'message': message}
		return res
class StockMove(models.Model):
	_inherit = "stock.move"
	_description = 'Stock Move'
	@api.model
	def create(self, vals):
		# print("--------------------------create--------------")
		res = super(StockMove, self).create(vals)
		res.onchange_product()
		res.onchange_product_id()
		res._onchange_lot_ids()
		res.onchange_move_line_ids()
		res.onchange_product_uom()
		return res