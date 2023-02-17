from odoo import _, api, fields, models


class EngineModel(models.Model):
    _name = 'engine.model'
    _description = 'Engine Model for Equipment'

    name = fields.Char(string='Engine Model')
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Html(string='Notes')
    sequence = fields.Integer(string='Sequence')
    equipment_count = fields.Integer(string='Equipments')  # compute
