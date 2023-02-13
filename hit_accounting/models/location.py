# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Location(models.Model):
    _name = 'location'
    _description = 'Location'

    name = fields.Char('Name')
    active = fields.Boolean(string='Active', default=True)
    code = fields.Char('Code')
    location = fields.Char('Location')
