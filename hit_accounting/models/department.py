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
