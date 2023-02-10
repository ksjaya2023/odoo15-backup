from odoo import _, api, fields, models


class ReturnRequest(models.Model):
    _name = 'return.request'
    _description = 'Return Request'

    reservation_id = fields.Many2one(
        comodel_name='reservation', string='Reservation')
