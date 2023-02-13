from odoo import models, fields, api


class StockType(models.Model):
    _name = 'stock.type'
    _description = 'Stock Type'

    active = fields.Boolean(string='Active')
    name = fields.Char(string='Code')
    description = fields.Char(string='Description')
    sequence = fields.Integer(string='Sequence')
