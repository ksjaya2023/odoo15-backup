from odoo import _, api, fields, models


class EquipmentAttachment(models.Model):
    _name = 'eqp.attachment'
    _description = 'Attachment for Equipment'

    name = fields.Char(string='Attachment')
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Html(string='Notes')
    sequence = fields.Integer(string='Sequence')
    equipment_count = fields.Integer(string='Equipments')  # compute
