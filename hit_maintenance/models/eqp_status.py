from odoo import _, api, fields, models


class EquipmentStatus(models.Model):
    _name = 'eqp.status'
    _description = 'Status for Equipment'

    name = fields.Char(string='Status')
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Html(string='Notes')
    sequence = fields.Integer(string='Sequence')
    equipment_count = fields.Integer(
        string='Equipments', compute='_compute_equipment_count')

    @api.depends('name')
    def _compute_equipment_count(self):
        for record in self:
            record.equipment_count = self.env['maintenance.equipment'].search_count(
                [('class_id', '=', record.id)])

    def test_connection(self):
        title = _("Connection Test Succeeded!")
        message = _("Everything seems properly set up!")
        action = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'sticky': False,
            }
        }
        return action
