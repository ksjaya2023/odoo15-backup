
# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'account.payment'

    account_move_id = fields.Many2one('account.move', string='Invoice Number')
    advance = fields.Boolean('Advance')

    @api.onchange('payment_type')
    def _onchange_payment_type(self):
        domain = []
        if self.payment_type == 'inbound':
            domain = [('move_type', '=', 'out_invoice'),
                      ('state', '=', 'posted')]
        elif self.payment_type == 'outbound':
            domain = [('move_type', '=', 'in_invoice'),
                      ('state', '=', 'posted')]
        self.account_move_id = False
        return {'domain': {'account_move_id': domain}}

    def action_post(self):
        ''' draft -> posted '''
        self.move_id._post(soft=False)

        self.filtered(
            lambda pay: pay.is_internal_transfer and not pay.paired_internal_transfer_payment_id
        )._create_paired_internal_transfer_payment()

        if self.advance:
            currency_id = self.move_id.currency_id
            amount = self.amount
            line_vals_list = []
            bank_account = self.journal_id.default_account_id
            if self.payment_type == 'inbound':
                advance_sales_account = self.partner_id.x_studio_advance_sales_id
                line_vals_list = [
                    {
                        'move_id' : self.move_id.id,
                        'name': self.move_id.name,
                        'date_maturity': self.date,
                        'amount_currency': amount,
                        'currency_id': currency_id.id,
                        'debit': amount,
                        'credit': 0.0,
                        'partner_id': self.partner_id.id,
                        'account_id': bank_account.id,
                    },
                    {
                        'move_id' : self.move_id.id,
                        'name': self.move_id.name,
                        'date_maturity': self.date,
                        'amount_currency': amount,
                        'currency_id': currency_id.id,
                        'debit': 0.0,
                        'credit': amount,
                        'partner_id': self.partner_id.id,
                        'account_id': advance_sales_account.id,
                    },
                ]
            else:
                advance_purchase_account = self.partner_id.x_studio_advance_purchase_id
                line_vals_list = [
                    {
                        'move_id' : self.move_id.id,
                        'name': self.move_id.name,
                        'date_maturity': self.date,
                        'amount_currency': amount,
                        'currency_id': currency_id.id,
                        'debit': amount,
                        'credit': 0.0,
                        'partner_id': self.partner_id.id,
                        'account_id': advance_purchase_account.id,
                    },
                    {
                        'move_id' : self.move_id.id,
                        'name': self.move_id.name,
                        'date_maturity': self.date,
                        'amount_currency': amount,
                        'currency_id': currency_id.id,
                        'debit': 0.0,
                        'credit': amount,
                        'partner_id': self.partner_id.id,
                        'account_id': bank_account.id,
                    },
                ]

            self.env['account.move.line'].sudo().create(line_vals_list)


