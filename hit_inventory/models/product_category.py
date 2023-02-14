from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = 'product.category'
    _description = 'Product Category'

    category_description = fields.Char(string='Category Description')