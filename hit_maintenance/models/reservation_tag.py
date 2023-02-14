from odoo import _, api, fields, models


class ReservationTag(models.Model):
    _name = 'reservation.tag'
    _description = 'Reservation Tag'
    _order = 'sequence, id'

    name = fields.Char(string='Name', translate=True)
    sequence = fields.Integer(string='Sequence', default=10)
    color = fields.Char(string='Color Index')
