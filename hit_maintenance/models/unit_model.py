from odoo import _, api, fields, models


class UnitModel(models.Model):
    _name = 'unit.model'
    _description = 'Unit Model for Equipment'

    name = fields.Char(string='Unit Model/EGI')
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Html(string='Notes')
    sequence = fields.Integer(string='Sequence')
    equipment_count = fields.Integer(
        string='Equipments', compute='_compute_equipment_count')

    @api.depends('name')
    def _compute_equipment_count(self):
        for record in self:
            record.equipment_count = self.env['maintenance.equipment'].search_count(
                [('unit_model_id', '=', record.id)])
