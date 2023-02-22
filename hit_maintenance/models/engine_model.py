from odoo import _, api, fields, models


class EngineModel(models.Model):
    _name = 'engine.model'
    _description = 'Engine Model for Equipment'

    name = fields.Char(string='Engine Model')
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Html(string='Notes')
    sequence = fields.Integer(string='Sequence')
    equipment_count = fields.Integer(
        string='Equipments', compute='_compute_equipment_count')

    @api.depends('name')
    def _compute_equipment_count(self):
        for record in self:
            record.equipment_count = self.env['maintenance.equipment'].search_count(
                [('engine_model_id', '=', record.id)])
