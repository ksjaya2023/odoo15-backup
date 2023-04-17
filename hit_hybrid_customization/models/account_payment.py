
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

    # def action_post(self):
    #     if self.advance:
    #         move_vals = [
    #             {
    #                 'journal_id' : self.journal_id.id,
    #                 'date' : self.date
    #             }
    #         ]
    #         move_id = self.env['account.move'].sudo().create(move_vals)
    #         currency_id = self.move_id.currency_id
    #         amount = self.amount
    #         line_vals_list = []
    #         bank_account = self.journal_id.default_account_id
    #         if self.payment_type == 'inbound':
    #             advance_sales_account = self.partner_id.x_studio_advance_sales_id
    #             line_vals_list = [
    #                 {
    #                     'move_id' : move_id.id,
    #                     'name': self.move_id.name,
    #                     'date_maturity': self.date,
    #                     'amount_currency': amount,
    #                     'currency_id': currency_id.id,
    #                     'debit': amount,
    #                     'credit': 0.0,
    #                     'partner_id': self.partner_id.id,
    #                     'account_id': bank_account.id,
    #                 },
    #                 {
    #                     'move_id' : move_id.id,
    #                     'name': self.move_id.name,
    #                     'date_maturity': self.date,
    #                     'amount_currency': amount,
    #                     'currency_id': currency_id.id,
    #                     'debit': 0.0,
    #                     'credit': amount,
    #                     'partner_id': self.partner_id.id,
    #                     'account_id': advance_sales_account.id,
    #                 },
    #             ]
    #         else:
    #             advance_purchase_account = self.partner_id.x_studio_advance_purchase_id
    #             line_vals_list = [
    #                 {
    #                     'move_id' : move_id.id,
    #                     'name': self.move_id.name,
    #                     'date_maturity': self.date,
    #                     'amount_currency': amount,
    #                     'currency_id': currency_id.id,
    #                     'debit': amount,
    #                     'credit': 0.0,
    #                     'partner_id': self.partner_id.id,
    #                     'account_id': advance_purchase_account.id,
    #                 },
    #                 {
    #                     'move_id' : move_id.id,
    #                     'name': self.move_id.name,
    #                     'date_maturity': self.date,
    #                     'amount_currency': amount,
    #                     'currency_id': currency_id.id,
    #                     'debit': 0.0,
    #                     'credit': amount,
    #                     'partner_id': self.partner_id.id,
    #                     'account_id': bank_account.id,
    #                 },
    #             ]

    #         self.env['account.move.line'].sudo().create(line_vals_list)
    #         move_id._post(soft=False)

    #     ''' draft -> posted '''
    #     self.move_id._post(soft=False)

    #     self.filtered(
    #         lambda pay: pay.is_internal_transfer and not pay.paired_internal_transfer_payment_id
    #     )._create_paired_internal_transfer_payment()

    # @api.depends('journal_id', 'payment_type', 'payment_method_line_id','advance')
    # def _compute_outstanding_account_id(self):
    #     for pay in self:
    #         if pay.advance:
    #             if pay.payment_type == 'inbound':
    #                 pay.outstanding_account_id = pay.partner_id.x_studio_advance_sales_id
    #             elif pay.payment_type == 'outbound':
    #                 pay.outstanding_account_id = pay.partner_id.x_studio_advance_purchase_id
    #             else:
    #                 pay.outstanding_account_id = False
    #         else
    #             if pay.payment_type == 'inbound':
    #                 pay.outstanding_account_id = (pay.payment_method_line_id.payment_account_id
    #                                               or pay.journal_id.company_id.account_journal_payment_debit_account_id)
    #             elif pay.payment_type == 'outbound':
    #                 pay.outstanding_account_id = (pay.payment_method_line_id.payment_account_id
    #                                               or pay.journal_id.company_id.account_journal_payment_credit_account_id)
    #             else:
    #                 pay.outstanding_account_id = False

    @api.depends('journal_id', 'partner_id', 'partner_type', 'is_internal_transfer','advance')
    def _compute_destination_account_id(self):
        self.destination_account_id = False
        for pay in self:
            if pay.is_internal_transfer:
                pay.destination_account_id = pay.journal_id.company_id.transfer_account_id
            elif pay.partner_type == 'customer':
                # Receive money from invoice or send money to refund it.
                if pay.partner_id:
                    if pay.advance:
                        if pay.payment_type == 'inbound':
                            pay.destination_account_id = pay.partner_id.x_studio_advance_sales_id
                        else:
                            pay.destination_account_id = pay.partner_id.x_studio_advance_purchase_id
                    else:
                        pay.destination_account_id = pay.partner_id.with_company(pay.company_id).property_account_receivable_id
                else:
                    pay.destination_account_id = self.env['account.account'].search([
                        ('company_id', '=', pay.company_id.id),
                        ('internal_type', '=', 'receivable'),
                        ('deprecated', '=', False),
                    ], limit=1)
            elif pay.partner_type == 'supplier':
                # Send money to pay a bill or receive money to refund it.
                if pay.partner_id:
                    if pay.advance:
                        if pay.payment_type == 'inbound':
                            pay.destination_account_id = pay.partner_id.x_studio_advance_sales_id
                        else:
                            pay.destination_account_id = pay.partner_id.x_studio_advance_purchase_id
                    else:
                        pay.destination_account_id = pay.partner_id.with_company(pay.company_id).property_account_payable_id
                else:
                    pay.destination_account_id = self.env['account.account'].search([
                        ('company_id', '=', pay.company_id.id),
                        ('internal_type', '=', 'payable'),
                        ('deprecated', '=', False),
                    ], limit=1)