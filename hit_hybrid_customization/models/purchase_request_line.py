# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    life_of_projects = fields.Selection([
        ('3_bulan', '3 Bulan'),
        ('6_bulan', '6 Bulan'),
        ('9_bulan', '9 Bulan'),
        ('12_bulan', '12 Bulan'),
        ('15_bulan', '15 Bulan'),
        ('18_bulan', '18 Bulan'),
        ('21_bulan', '21 Bulan'),
        ('24_bulan', '24 Bulan'),
        ('27_bulan', '27 Bulan'),
        ('30_bulan', '30 Bulan'),
        ('33_bulan', '33 Bulan'),
        ('36_bulan', '36 Bulan'),
        ('39_bulan', '39 Bulan'),
        ('42_bulan', '42 Bulan'),
        ('45_bulan', '45 Bulan'),
        ('48_bulan', '48 Bulan'),
        ('51_bulan', '51 Bulan'),
        ('54_bulan', '54 Bulan'),
        ('58_bulan', '58 Bulan'),
        ('60_bulan', '60 Bulan'),
    ], string='Life of Projects')
