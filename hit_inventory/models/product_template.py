from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    bin_location = fields.Many2one(
        comodel_name='bin_location', string='Bin Location')
    product_class = fields.Many2one(
        comodel_name='product.class', string='Product Class')
    stock_type = fields.Many2one(
        comodel_name='stock.type', string='Stock Type')
