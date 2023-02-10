from odoo import _, api, fields, models


class Mnemonic(models.Model):
    _name = 'mnemonic'
    _description = 'Mnemonic for Equipment'

    name = fields.Char(string='Mnemonic')
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Html(string='Notes')
    sequence = fields.Integer(string='Sequence')
