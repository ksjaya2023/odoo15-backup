# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ActivityLocation(models.Model):
    _name = 'activity.location'
    _description = 'Activity Location'

    name = fields.Char('Name')
    active = fields.Boolean(string='Active', default=True)
    code = fields.Char('Code')
    sequence = fields.Integer(string='Sequence')
    process_activity_id = fields.Many2one(
        'process.line', string='Activity')
    activity_description = fields.Char(
        'Activity Description', related='process_activity_id.activity_description')
    location_department_ids = fields.One2many(
        'activity.location.department', 'activity_location_id', string='Location Department')
    location_id = fields.Many2one('location', string='Location')
    location_description = fields.Char(
        'Location Description', related='location_id.location')

    @api.onchange('process_activity_id', 'location_id')
    def _onchange_activity_location_form(self):
        for record in self:
            record.name = str(record.process_activity_id.process_id.code) + \
                '-' + str(record.process_activity_id.activity_id.code) + \
                '-' + str(record.location_id.code) + \
                ': ' + str(record.location_description)


class ActivitylocationDepartment(models.Model):
    _name = 'activity.location.department'
    _description = 'Location Department'

    name = fields.Char('Name', compute='_compute_name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')
    activity_location_id = fields.Many2one(
        'activity.location', string='Location')
    location_description = fields.Char(
        'Location Description', related='department_id.department')
    department_id = fields.Many2one('department', string='Department')
    department_description = fields.Char(
        'Department Description', related='department_id.department')

    @api.onchange('activity_location_id', 'department_id')
    def _onchange_(self):
        for record in self:
            record.name = str(record.activity_location_id.process_activity_id.process_id.code) + \
                '-' + str(record.activity_location_id.process_activity_id.activity_id.code) + \
                '-' + str(record.activity_location_id.location_id.code) + \
                '-' + str(record.department_id.code) + \
                ': ' + str(record.department_description)

    @api.depends('activity_location_id', 'department_id')
    def _compute_name(self):
        for record in self:
            record.name = str(record.activity_location_id.process_activity_id.process_id.code) + \
                '-' + str(record.activity_location_id.process_activity_id.activity_id.code) + \
                '-' + str(record.activity_location_id.location_id.code) + \
                '-' + str(record.department_id.code) + \
                ': ' + str(record.department_description)
