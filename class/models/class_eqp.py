# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Class(models.Model):
    _name = 'Class'
    _description = 'Class'

    name = fields.Char(string='Class Id')
    active = fields.Boolean()
    studio_active = fields.Boolean(string='Active')
    studio_description = fields.Char(string='EQP Type')
    studio_notes = fields.Html(string='Notes')
    studio_sequence = fields.Integer(string='Sequence')
    class_maintenance_equipment_count = fields.Integer(string='Equipment')