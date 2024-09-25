from odoo import models, fields

class ProductType(models.Model):
    _name = 'product.type'

    name = fields.Char("name")

