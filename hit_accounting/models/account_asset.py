# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    asset_description = fields.Char('Asset Description')
