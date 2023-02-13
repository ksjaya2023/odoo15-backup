# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductClass(models.Model):
    _name = 'product_class'
    _description = 'product_class'

    name = fields.Char(string='Code')
    description= fields.Char(string='Description')