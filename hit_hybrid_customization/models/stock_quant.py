from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class StockQuant(models.Model):
    _inherit = "stock.quant"

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')

    @api.model
    def _get_inventory_fields_create(self):
        """(Inherited Function) Returns a list of fields user can edit when he want to create a quant in `inventory_mode`."""
        fields = super(StockQuant, self)._get_inventory_fields_create()
        fields.extend(["analytic_account_id"])  # custom fields
        return fields

    @api.model
    def _get_inventory_fields_write(self):
        """(Inherited Function) Returns a list of fields user can edit when he want to edit a quant in `inventory_mode`."""
        fields = super(StockQuant, self)._get_inventory_fields_write()
        fields.extend(["analytic_account_id"])  # custom fields
        return fields

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


