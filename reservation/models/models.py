# -*- coding: utf-8 -*-

from odoo import models, fields, api


class reservation(models.Model):
    _name = 'reservation'
    _description = 'reservation'

    name = fields.Char()
