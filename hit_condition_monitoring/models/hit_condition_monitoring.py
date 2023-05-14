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

    name = fields.Char('Name', default='Draft', readonly=True)
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment')
    work_order_type = fields.Selection(selection=[
        ('Maintenance', 'Service'),
        ('Perbaikan', 'Repaired'),
        ('Backlog', 'Backlog'),
    ],
        string='Work Order Type',
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
    attachment = fields.Binary('Upload File')
    attachment_name = fields.Char('Attachment Name')
    work_order_id = fields.Many2one('maintenance.request', string='Work Order')
    show_maintenance_request = fields.Boolean(
        'Show Maintenance Request', default=False, compute='_compute_show_maintenance_request')

    @api.depends('name')
    def _compute_show_maintenance_request(self):
        if not self.name:
            self.show_maintenance_request = False
        else:
            self.show_maintenance_request = True

    def seq_auto_name(self):
        seq = self.env['ir.sequence'].next_by_code(
            'condition.monitoring.seq')
        return self.write({"name": seq})

    @api.model
    def create(self, vals):
        create_data = super(HitConditionMonitoring, self).create(vals)
        create_data.seq_auto_name()
        self.show_maintenance_request = False
        return create_data

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

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        for record in self:
            if record.equipment_id:
                record.location_id = record.equipment_id.x_studio_warehouse.id
                record.warehouse_id = record.equipment_id.x_studio_locations.id
                record.hourmeter = record.equipment_id.x_studio_current_hrm

    def create_new_request(self):
        condition_monitoring_data = {
            'inspection_id': self.id,
            'equipment_id': self.equipment_id.id or None,
            'x_studio_maintenance_type': self.maintenance_type or None,
            'maintenance_team_id': self.maintenance_team_id.id or None,
            'company_id': self.env.company.id,
            'user_id': self.responsible_id.id or None,
            'x_studio_attachment': self.attachment or None,
            'x_studio_work_order_type': self.work_order_type or None,
            'schedule_date': self.schedule_date or None,
        }
        maintenance_requests = self.env["maintenance.request"].create(
            condition_monitoring_data)
        self.write({"work_order_id": maintenance_requests.id})
        return maintenance_requests
