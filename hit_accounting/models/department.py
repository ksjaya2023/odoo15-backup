# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Department(models.Model):
    _name = 'hit.department'
    _description = 'Department'

    name = fields.Char('Name')
    active = fields.Boolean(string='Active', default=True)
    code = fields.Char('Code')
    department = fields.Char('Department')

    @api.onchange('code', 'department')
    def _onchange_(self):
        for record in self:
            record.name = str(record.code) + ' ' + str(record.department)


class DepartmentAnalytic(models.Model):
    _name = 'hit.department.analytic'
    _description = 'Department Analytic'

    name = fields.Char('Name')
    active = fields.Boolean(string='Active', default=True)
    # account_analytic_group_id = fields.Many2one(
    #     'account.analytic.group', string='Account Analytic Group')
    company_id = fields.Many2one('res.company', string='Company')
    department_id = fields.Many2one(
        'hit.activity.location.department', string='Department')
    department_description = fields.Char('Department Description')
    description = fields.Text('Description')

    @api.onchange('department_id')
    def _onchange_department_id(self):
        for record in self:
            record.name = record.department_id.name + 'AAG'
