# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductClass(models.Model):
    _name = 'product.class'
    _description = 'Product Class'

    name = fields.Char(string='Code')
    description = fields.Char(string='Description')
