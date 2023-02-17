# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    brand_id = fields.Many2one('brand', string='brand')
    part_number = fields.Char('Part Number')
    product_id = fields.Integer('Product ID')
    stock_code = fields.Char('Stock Code')
