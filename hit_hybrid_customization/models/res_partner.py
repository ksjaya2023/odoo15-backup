# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    advance_sales_id = fields.Many2one(
        'account.account', string='Advance Sales')
    advance_purchase_id = fields.Many2one(
        'account.account', string='Advance Purchase')
