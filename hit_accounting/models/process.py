# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Process(models.Model):
    _name = 'process'
    _description = 'Process'

    name = fields.Char('Process')
    active = fields.Boolean(string='Active', default=True)
    code = fields.Char('Code')
    description = fields.Char('Description')
    process_ids = fields.One2many(
        'process.line', 'process_id', string='Process IDS')

    @api.onchange('code', 'description')
    def _onchange_(self):
        for record in self:
            record.name = str(record.code) + ' ' + str(record.description)


class ProcessLine(models.Model):
    _name = 'process.line'
    _description = 'Process Activity'

    name = fields.Char('Process', compute='_compute_name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')
    process_id = fields.Many2one('process', string='Process ID')
    process_description = fields.Char(
        'Process Description', related='process_id.description')
    activity_id = fields.Many2one('activity', string='Activity')
    activity_description = fields.Char(
        'Activity Description', related='activity_id.activity')
    process_activity_ids = fields.One2many(
        'activity.location', 'process_activity_id', string='Process Activity')

    @api.onchange('process_id', 'activity_id')
    def _onchange_(self):
        for record in self:
            record.name = str(record.process_id.code) + '-' + str(
                record.activity_id.code) + ': ' + str(record.activity_description)

    @api.depends('process_id', 'activity_id')
    def _compute_name(self):
        for record in self:
            record.name = str(record.process_id.code) + '-' + str(
                record.activity_id.code) + ': ' + str(record.activity_description)
