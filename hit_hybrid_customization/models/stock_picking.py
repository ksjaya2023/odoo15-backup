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

    # def auto_input_allocation_from_backorder(self, backorder_picking):
    #     _logger.info('auto_input_allocation_from_backorder')
    #     picking_id = self.env['stock.picking'].browse(backorder_picking.id)
    #     purchase_request_id = picking_id.purchase_request_id
    #     purchase_id = picking_id.purchase_id
    #     picking_items = picking_id.move_ids_without_package
        
    #     for item in picking_items:
    #         operation_category = item.operation_category
    #         product_id = item.product_id.id
    #         quantity = item.product_uom_qty
    #         uom = item.product_uom.id
            
    #         if not purchase_request_id or not purchase_id or not product_id:
    #             continue
            
    #         pr_line_id = self.env['purchase.request.line'].search([
    #             ('request_id', '=', purchase_request_id.id),
    #             ('product_id', '=', product_id)
    #         ])
            
    #         po_line_id = self.env['purchase.order.line'].search([
    #             ('order_id', '=', purchase_id.id),
    #             ('product_id', '=', product_id)
    #         ])
            
    #         if not pr_line_id or not po_line_id:
    #             continue
            
    #         if operation_category == 'rev':
    #             quantity = 0
    #         elif operation_category == 'in':
    #             quantity = 0
    #         else:
    #             return False
            
    #         allocation_value = {
    #             'purchase_request_line_id': pr_line_id.id or False,
    #             'purchase_line_id': po_line_id.id or False,
    #             'stock_move_id': item.id or False,
    #             'product_uom_id': uom,
    #             'requested_product_uom_qty': quantity,
    #             'allocated_product_qty': quantity,
    #         }
            
    #         try:
    #             self.env['purchase.request.allocation'].create(allocation_value)
    #         except Exception as e:
    #             # Handle the exception (log, display error, etc.)
    #             continue
        
    #     return True


    # ---- Inherited Functions ----
    @api.depends('state', 'operation_category')
    def _compute_show_validate(self):
        for picking in self:
            super(StockPicking, picking)._compute_show_validate()
            if picking.state == 'assigned' and picking.operation_category == 'rev' and picking.x_studio_still_in_approval == True:
                picking.show_validate = False

    # def _create_backorder(self):
    #     _logger.info('_create_backorder custom')
    #     """ This method is called when the user chose to create a backorder. It will create a new
    #     picking, the backorder, and move the stock.moves that are not `done` or `cancel` into it.
    #     """
    #     backorders = self.env['stock.picking']
    #     bo_to_assign = self.env['stock.picking']
    #     for picking in self:
    #         moves_to_backorder = picking.move_lines.filtered(lambda x: x.state not in ('done', 'cancel'))
    #         if moves_to_backorder:
    #             _logger.info('Creating backorder for picking: %s' % picking.name)
    #             backorder_picking = picking.copy({
    #                 'name': '/',
    #                 'move_lines': [],
    #                 'move_line_ids': [],
    #                 'backorder_id': picking.id
    #             })
    #             _logger.info('Backorder created with name: %s' % backorder_picking.name)
    #             picking.message_post(
    #                 body=_('The backorder <a href=# data-oe-model=stock.picking data-oe-id=%d>%s</a> has been created.') % (
    #                     backorder_picking.id, backorder_picking.name))
    #             moves_to_backorder.write({'picking_id': backorder_picking.id})
    #             moves_to_backorder.move_line_ids.package_level_id.write({'picking_id':backorder_picking.id})
    #             moves_to_backorder.mapped('move_line_ids').write({'picking_id': backorder_picking.id})
    #             backorders |= backorder_picking
    #             self.auto_input_allocation_from_backorder(backorder_picking)
    #             if backorder_picking.picking_type_id.reservation_method == 'at_confirm':
    #                 bo_to_assign |= backorder_picking
    #     if bo_to_assign:
    #         bo_to_assign.action_assign()
    #     return backorders                


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
        date = self._context.get('force_period_date', fields.Date.context_today(self))
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

    

