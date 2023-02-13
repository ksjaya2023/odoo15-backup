# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    bank_account_name = fields.Char('Bank Account Name')
    bank_address_branches = fields.Char('Bank Address Branches')
    pic_name = fields.Char('PIC Name')
