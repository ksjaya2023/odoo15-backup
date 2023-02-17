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
    activity_description = fields.Char('Activity Description')
    location_department_ids = fields.One2many(
        'activity.location.department', 'activity_location_id', string='Location Department')
    location_id = fields.Many2one('location', string='Location')
    location_description = fields.Char('Location Description')  # related
    process = fields.Char('Process')


class ActivitylocationDepartment(models.Model):
    _name = 'activity.location.department'
    _description = 'Location Department'

    name = fields.Char('Name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')
    activity_location_id = fields.Many2one(
        'activity.location', string='Location')
    activity = fields.Char('Activity')  # related
    department_id = fields.Many2one('department', string='Department')
    department_description = fields.Char('Department Description')
    location_description = fields.Char('Location Description')  # related
    process = fields.Char('Process')  # related
