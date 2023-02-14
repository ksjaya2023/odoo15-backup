from odoo import _, api, fields, models


class EquipmentAttachmentProduct(models.Model):
    _name = 'eqp.attachment.product'
    _description = 'Attachment Product for Equipment'

    name = fields.Char(string='Attachment Product')
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Html(string='Notes')
    sequence = fields.Integer(string='Sequence')
    equipment_count = fields.Integer(string='Equipments')  # compute
