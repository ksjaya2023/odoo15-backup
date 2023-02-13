# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Department(models.Model):
    _name = 'department'
    _description = 'Department'

    name = fields.Char('Name')
    active = fields.Boolean(string='Active', default=True)
    code = fields.Char('Code')
    department = fields.Char('Department')
    department_ids = fields.One2many(
        'department.line', 'department_id', string='Department IDS')


class DepartmentLine(models.Model):
    _name = 'department.line'
    _description = 'Department Line'

    name = fields.Char('Name')
    sequence = fields.Integer(string='Sequence')
    department_id = fields.Many2one('department', string='department')
