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


class DepartmentAnalytic(models.Model):
    _name = 'department.analytic'
    _description = 'Department Analytic'

    name = fields.Char('Name')
    active = fields.Boolean(string='Active', default=True)
    # account_analytic_group_id = fields.Many2one(
    #     'account.analytic.group', string='Account Analytic Group')
    company_id = fields.Many2one('res.company', string='Company')
    department_id = fields.Many2one(
        'activity.location.department', string='Department')
    department_description = fields.Char('Department Description')
    description = fields.Text('Description')
