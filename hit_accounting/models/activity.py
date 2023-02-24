# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Activity(models.Model):
    _name = 'activity'
    _description = 'Activity'

    name = fields.Char('Name')
    active = fields.Boolean(string='Active', default=True)
    code = fields.Char('Code')
    activity = fields.Char('Activity')

    @api.onchange('code')
    def _onchange_(self):
        for record in self:
            record.name = str(record.code)


class ActivityLine(models.Model):
    _name = 'activity.line'
    _description = 'Activity Line'

    name = fields.Char('Name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')
