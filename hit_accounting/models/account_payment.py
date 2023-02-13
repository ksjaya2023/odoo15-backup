# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # Maybe some of them are related
    agreement_date = fields.Date('Agreement Date')
    agreement_doc = fields.Char('Agreement Doc')
    account_ids = fields.Many2many('account.account', string='Account')
    users_ids = fields.Many2many('res.users', string='Users')
    nomer_faktur = fields.Char('Nomer Faktur')
    payment_voucher = fields.Char('Payment Voucher')
    tanggal_bukti_potong = fields.Date('Tanggal Bukti Potong')
    tanggal_faktur_pajak = fields.Date('Tanggal Faktur Pajak')
