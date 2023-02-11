from odoo import _, api, fields, models


class ReservationStage(models.Model):
    _name = 'reservation.stage'
    _description = 'Reservation Stage'
    _order = 'sequence, id'

    name = fields.Char(string='Name', translate=True)
    sequence = fields.Integer(string='Sequence', default=10)
    fold = fields.Boolean(string='Folded in Kanban View',
                          help='This stage is folded in the kanban view when'
                               'there are no records in that stage to display.')
    color = fields.Char(string='Color Index')
