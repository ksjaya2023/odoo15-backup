# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    site_id = fields.Many2one('md.site', string='Site')

    def button_confirm_rfq(self):
        self.write({'state': 'sent'})


    def _prepare_invoice(self):
        invoice_vals = super(PurchaseOrder, self)._prepare_invoice()
        site_id = self.site_id.id
        invoice_vals.update({'site_id': site_id})
        return invoice_vals


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'


    @api.constrains('account_analytic_id')
    def _constrains_account_analytic_id(self):
        for record in self:
            if not record.account_analytic_id:
                raise ValidationError(_('The analytic account requires mandatory input.'))
    


