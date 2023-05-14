# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Hourmeter(models.Model):
    _name = 'hourmeter'
    _description = 'Hourmeter'

    name = fields.Char(string='Status')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')
