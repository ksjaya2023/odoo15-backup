from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import groupby
from odoo.tools.float_utils import float_compare, float_is_zero
import datetime

import logging
_logger = logging.getLogger(__name__)




class StockQuant(models.Model):
    _inherit = "stock.quant"

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    backdate_inventory = fields.Datetime('Backdate Inventory')

    @api.model
    def _get_inventory_fields_create(self):
        """(Inherited Function) Returns a list of fields user can edit when he want to create a quant in `inventory_mode`."""
        res = super()._get_inventory_fields_create()
        res += ["analytic_account_id", "accounting_date", "backdate_inventory"]
        return res

    @api.model
    def _get_inventory_fields_write(self):
        """(Inherited Function) Returns a list of fields user can edit when he want to edit a quant in `inventory_mode`."""
        res = super()._get_inventory_fields_write()
        res += ["analytic_account_id", "accounting_date", "backdate_inventory"]
        return res

    def _get_inventory_move_values(self, qty, location_id, location_dest_id, out=False):
        """ Called when user manually set a new quantity (via `inventory_quantity`)
        just before creating the corresponding stock move.

        :param location_id: `stock.location`
        :param location_dest_id: `stock.location`
        :param out: boolean to set on True when the move go to inventory adjustment location.
        :return: dict with all values needed to create a new `stock.move` with its move line.
        """
        self.ensure_one()
        if fields.Float.is_zero(qty, 0, precision_rounding=self.product_uom_id.rounding):
            name = _('Product Quantity Confirmed')
        else:
            name = _('Product Quantity Updated')
        return {
            'name': self.env.context.get('inventory_name') or name,
            'product_id': self.product_id.id,
            'product_uom': self.product_uom_id.id,
            'product_uom_qty': qty,
            'company_id': self.company_id.id or self.env.company.id,
            'state': 'confirmed',
            'location_id': location_id.id,
            'location_dest_id': location_dest_id.id,
            'is_inventory': True,
            'analytic_account_id': self.analytic_account_id.id or False,
            'move_line_ids': [(0, 0, {
                'product_id': self.product_id.id,
                'product_uom_id': self.product_uom_id.id,
                'qty_done': qty,
                'location_id': location_id.id,
                'location_dest_id': location_dest_id.id,
                'company_id': self.company_id.id or self.env.company.id,
                'lot_id': self.lot_id.id,
                'package_id': out and self.package_id.id or False,
                'result_package_id': (not out) and self.package_id.id or False,
                'owner_id': self.owner_id.id,
            })]
        }

    def _apply_inventory(self):
        backdate = self.backdate_inventory
        move_vals = []
        if not self.user_has_groups('stock.group_stock_manager'):
            raise UserError(_('Only a stock manager can validate an inventory adjustment.'))
        for quant in self:
            # Create and validate a move so that the quant matches its `inventory_quantity`.
            if float_compare(quant.inventory_diff_quantity, 0, precision_rounding=quant.product_uom_id.rounding) > 0:
                move_vals.append(
                    quant._get_inventory_move_values(quant.inventory_diff_quantity,
                                                     quant.product_id.with_company(quant.company_id).property_stock_inventory,
                                                     quant.location_id))
            else:
                move_vals.append(
                    quant._get_inventory_move_values(-quant.inventory_diff_quantity,
                                                     quant.location_id,
                                                     quant.product_id.with_company(quant.company_id).property_stock_inventory,
                                                     out=True))
        moves = self.env['stock.move'].with_context(inventory_mode=False).create(move_vals)
        moves._action_done()
        if backdate:
            moves.write({'date': self.backdate_inventory})
            sml = self.env['stock.move.line'].search([('move_id', '=', moves.id), ('reference', '=', 'Product Quantity Updated')], limit=1)
            if sml:
                sml.write({'date': self.backdate_inventory})
        self.location_id.write({'last_inventory_date': fields.Date.today()})
        date_by_location = {loc: loc._get_next_inventory_date() for loc in self.mapped('location_id')}
        for quant in self:
            quant.inventory_date = date_by_location[quant.location_id]
        self.write({'inventory_quantity': 0, 'user_id': False})
        self.write({'inventory_diff_quantity': 0})





    



