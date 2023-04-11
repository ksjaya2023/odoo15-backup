
# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'account.payment'

    account_move_id = fields.Many2one('account.move', string='Invoice Number')

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
