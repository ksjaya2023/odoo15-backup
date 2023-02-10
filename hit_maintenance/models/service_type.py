from odoo import _, api, fields, models


class ServiceType(models.Model):
    _name = 'service.type'
    _description = 'Service Type'

    name = fields.Char(string='Status')
    active = fields.Boolean(string='Active')
    sequence = fields.Integer(string='Sequence')
    service_amount = fields.Integer(string='Service Amount')
