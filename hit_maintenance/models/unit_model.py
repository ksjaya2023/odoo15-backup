from odoo import _, api, fields, models


class UnitModel(models.Model):
    _name = 'unit.model'
    _description = 'Unit Model for Equipment'

    name = fields.Char(string='Unit Model/EGI')
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Html(string='Notes')
    sequence = fields.Integer(string='Sequence')
    equipment_count = fields.Integer(string='Equipments')  # compute
