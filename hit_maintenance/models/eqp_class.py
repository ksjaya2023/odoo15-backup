# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EquipmentClass(models.Model):
    _name = 'eqp.class'
    _description = 'Eqipment Class'

    name = fields.Char(string='Class Id')
    active = fields.Boolean(string='Active', default=True)
    description = fields.Char(string='Equipment Type')
    notes = fields.Html(string='Notes')
    sequence = fields.Integer(string='Sequence')
    equipment_count = fields.Integer(
        string='Equipment', compute='_compute_equipment_count')

    @api.depends('name')
    def _compute_equipment_count(self):
        for record in self:
            record.equipment_count = self.env['maintenance.equipment'].search_count(
                [('status_id', '=', record.id)])
