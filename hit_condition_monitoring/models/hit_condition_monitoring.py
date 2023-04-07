# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class HitConditionMonitoring(models.Model):
    _name = 'hit.condition.monitoring'
    _description = 'hit.condition.monitoring'

    def _get_default_team_id(self):
        MT = self.env['maintenance.team']
        team = MT.search([], limit=1)
        if not team:
            team = MT.search([], limit=1)
        return team.id

    name = fields.Char('Name', default='Draft')
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment')
    work_order_type = fields.Selection(selection=[
        ('Maintenance', 'Service'),
        ('Perbaikan', 'Repaired'),
        ('Backlog', 'Backlog'),
        ('Inspection', 'Inspection'),
    ],
        string='Work Order Type',
        default='Inspection',
    )
    maintenance_type = fields.Selection(selection=[
        ('Schedulle', 'Schedule'),
        ('Unschedulle', 'Unschedule'),
    ],
        string='Maintenance Type',
        default='Schedulle',
    )
    location_id = fields.Many2one('stock.warehouse', string='Location')
    warehouse_id = fields.Many2one('stock.location', string='Warehouse')
    maintenance_team_id = fields.Many2one(
        'maintenance.team', string='Team', required=True, default=_get_default_team_id)
    responsible_id = fields.Many2one(
        'res.users', string='Responsible')
    schedule_date = fields.Datetime('Schedule Date')
    complete_date = fields.Datetime('Complete Date')
    owner_user_id = fields.Many2one(
        'res.users', string='Created by User', default=lambda s: s.env.uid, readonly=True)
    hourmeter = fields.Char('Hourmeter')
    note = fields.Char('Note')
    attachment = fields.Binary('Upload PDF')
    attachment_name = fields.Char('Attachment Name')

    @api.onchange('maintenance_team_id')
    def _onchange_maintenance_team_id(self):
        if self.maintenance_team_id:
            user_ids = [
                user.id for user in self.maintenance_team_id.member_ids]
            domain = [('id', 'in', user_ids)]
            return {'domain': {'responsible_id': domain}}
        else:
            return {'domain': {'responsible_id': []}}

    @api.onchange('attachment')
    def onchange_attachment(self):
        if self.attachment:
            self.attachment_name = 'attachment_' + self.name
