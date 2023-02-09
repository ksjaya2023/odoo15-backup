# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BinLocation(models.Model):
    _name = 'bin_location'
    _description = 'bin_location'

    name = fields.Char()
