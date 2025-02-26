# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

_CATEGORY = [
    ("in", "Receipts"),
    ("int", "Internal Transfer"),
    ("out", "Inventory Issued"),
    ("rev", "Return to Vendor"),
    ("ret", "Returns"),
]


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    operation_category = fields.Selection(selection=_CATEGORY, string="Operation Category")



class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    site_id = fields.Many2one('md.site', string='Site') 


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    operation_category = fields.Selection(
        related="picking_type_id.operation_category",
        readonly=True,
        store=True,
        string="Operation Category",
    )

    purchase_request_id = fields.Many2one(
        "purchase.request",
        string="Purchase Request",
        readonly=True,
    )

    custom_backdate = fields.Date('Custom Backdate')

    # ---- Inherited Functions ----
    @api.depends('state', 'operation_category')
    def _compute_show_validate(self):
        for picking in self:
            super(StockPicking, picking)._compute_show_validate()
            if picking.state == 'assigned' and picking.operation_category == 'rev' and picking.x_studio_still_in_approval == True:
                picking.show_validate = False


class StockMove(models.Model):
    _inherit = 'stock.move'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')

    operation_category = fields.Selection(
        related="picking_id.operation_category",
        readonly=True,
        store=True,
        string="Operation Category",
    )


    def _prepare_account_move_vals(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id, cost):        
        self.ensure_one()
        # Customization for analytic account
        if self.is_inventory:
            analytic_account_id = self.analytic_account_id.id
        else:
            analytic_account_id = self.analytic_account_id.id

        move_lines = self._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, description, analytic_account_id)
        date = self.picking_id.custom_backdate or self._context.get('force_period_date', fields.Date.context_today(self))
        return {
            'journal_id': journal_id,
            'line_ids': move_lines,
            'date': date,
            'ref': description,
            'stock_move_id': self.id,
            'stock_valuation_layer_ids': [(6, None, [svl_id])],
            'move_type': 'entry',
        }

    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id, description, analytic_account_id=False):
        """
        Generate the account.move.line values to post to track the stock valuation difference due to the
        processing of the given quant.
        """
        self.ensure_one()

        # the standard_price of the product may be in another decimal precision, or not compatible with the coinage of
        # the company currency... so we need to use round() before creating the accounting entries.
        debit_value = self.company_id.currency_id.round(cost)
        credit_value = debit_value

        valuation_partner_id = self._get_partner_id_for_valuation_lines()
        res = [(0, 0, line_vals) for line_vals in self._generate_valuation_lines_data(valuation_partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description, analytic_account_id).values()] # Customization on this line

        return res


    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description, analytic_account_id=False):
        # This method returns a dictionary to provide an easy extension hook to modify the valuation lines (see purchase for an example)
        self.ensure_one()
        debit_line_vals = {
            'name': description,
            'product_id': self.product_id.id,
            'quantity': qty,
            'product_uom_id': self.product_id.uom_id.id,
            'ref': description,
            'partner_id': partner_id,
            'debit': debit_value if debit_value > 0 else 0,
            'credit': -debit_value if debit_value < 0 else 0,
            'account_id': debit_account_id,
            'analytic_account_id': analytic_account_id, # Customization on this line
        }

        credit_line_vals = {
            'name': description,
            'product_id': self.product_id.id,
            'quantity': qty,
            'product_uom_id': self.product_id.uom_id.id,
            'ref': description,
            'partner_id': partner_id,
            'credit': credit_value if credit_value > 0 else 0,
            'debit': -credit_value if credit_value < 0 else 0,
            'account_id': credit_account_id,
        }

        rslt = {'credit_line_vals': credit_line_vals, 'debit_line_vals': debit_line_vals}
        if credit_value != debit_value:
            # for supplier returns of product in average costing method, in anglo saxon mode
            diff_amount = debit_value - credit_value
            price_diff_account = self.product_id.property_account_creditor_price_difference

            if not price_diff_account:
                price_diff_account = self.product_id.categ_id.property_account_creditor_price_difference_categ
            if not price_diff_account:
                raise UserError(_('Configuration error. Please configure the price difference account on the product or its category to process this operation.'))

            rslt['price_diff_line_vals'] = {
                'name': self.name,
                'product_id': self.product_id.id,
                'quantity': qty,
                'product_uom_id': self.product_id.uom_id.id,
                'ref': description,
                'partner_id': partner_id,
                'credit': diff_amount > 0 and diff_amount or 0,
                'debit': diff_amount < 0 and -diff_amount or 0,
                'account_id': price_diff_account.id,
            }
        return rslt

    

