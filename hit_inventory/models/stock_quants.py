from odoo import models, fields, api


class StockQuants(models.Model):
    _inherit = 'stock.quant'
    _description = 'Quants'

    bin_location= fields.Many2one(comodel_name='bin_location', string='Bin Location')