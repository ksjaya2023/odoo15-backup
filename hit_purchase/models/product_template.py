# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    brand_id = fields.Many2one('brand', string='Brand')
    part_number = fields.Char('Part Number')
    stock_code = fields.Char('Stock Code')
