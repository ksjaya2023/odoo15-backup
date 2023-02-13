from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    bin_location = fields.Char(string='Bin Location')
    char_field_F5qLe = fields.Char(string='New Text')
    # many2one_bin_location = fields.Many2one(
    #     comodel_name='bin_location', string='Bin Location')
    # many2one_field_PQNRE = fields.Many2one(
    #     comodel_name='product_class', string='Product Class')
    # many2one_field_Ur0Py = fields.Many2one(
    #     comodel_name='stock_type', string='Stock Type')
    mnemonic_product = fields.Many2one(
        comodel_name='mnemonic', string='Mnemonic')
    part_number = fields.Char(string='Part Number')
    stock_code = fields.Char(string='Stock Code')
