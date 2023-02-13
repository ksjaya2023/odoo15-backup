# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BinLocation(models.Model):
    _name = 'bin.location'
    _description = 'Bin Location'

    name = fields.Char('Name')
