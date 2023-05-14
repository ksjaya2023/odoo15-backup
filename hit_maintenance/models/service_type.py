from odoo import _, api, fields, models


class ServiceType(models.Model):
    _name = 'service.type'
    _description = 'Service Type'

    name = fields.Char(string='Status', compute='_compute_name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')
    service_amount = fields.Integer(string='Service Amount')

    @api.depends('service_amount')
    def _compute_name(self):
        for record in self:
            record.name = str(record.service_amount)
