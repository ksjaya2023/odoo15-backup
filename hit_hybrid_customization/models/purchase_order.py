# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    site_id = fields.Many2one('md.site', string='Site')
    purchase_request_id = fields.Many2one(
        "purchase.request",
        string="Purchase Request",
        readonly=True,
    )
    total_discount = fields.Char(compute='_compute_total_discount', string='Total Discount')
    currency_symbol = fields.Char('Currency Symbol', related="currency_id.symbol")


    # ---- Computed Fields ----
        

    @api.depends('order_line')
    def _compute_total_discount(self):
        for record in self:
            total_discount_val = 0
            total_discount_val = sum(record.order_line.mapped("discount_val"))
            record.total_discount = total_discount_val


    # ---- Onchanges ----


    @api.onchange('order_line')
    def ktc_onchange_order_line(self):
        for rec in self:
            for line in rec.order_line:
                line.compute_discount()
                line.compute_discount_val()


    # ---- Buttons ----


    def button_confirm_rfq(self):
        self.write({'state': 'sent'})


    # ---- Inherited Functions ----


    def _prepare_picking(self):
        picking_vals = super(PurchaseOrder, self)._prepare_picking()
        picking_vals.update({"purchase_request_id": self.purchase_request_id.id or False})
        return picking_vals

    def _prepare_invoice(self):
        invoice_vals = super(PurchaseOrder, self)._prepare_invoice()
        site_id = self.site_id.id
        invoice_vals.update({'site_id': site_id})
        return invoice_vals


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    discount = fields.Float(string="Discount %")
    discount_val = fields.Float(string="Discount Value")


    def compute_discount_val(self):
        for record in self:
            if record.discount:
                record.discount_val = 0
                discount_val = (record.discount / 100) * (record.product_qty * record.price_unit)
                record.discount_val = discount_val


    def compute_discount(self):
        for record in self:
            if record.discount_val:
                record.discount = 0
                discount = (record.discount_val / (record.product_qty * record.price_unit)) * 100
                record.discount = discount


    # ---- Onchanges ----


    @api.onchange('discount','price_unit', 'product_qty')
    def _onchange_discount(self):
        self.compute_discount_val()


    @api.onchange('discount_val','price_unit', 'product_qty')
    def _onchange_discount_val(self):
        self.compute_discount()


    # ---- Constrains ----


    @api.constrains('account_analytic_id')
    def _constrains_account_analytic_id(self):
        for record in self:
            if not record.account_analytic_id:
                raise ValidationError(_('The analytic account requires mandatory input.'))


    # ---- Inherited Functions ----


    def _prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom):
        self.ensure_one()
        self._check_orderpoint_picking_type()
        product = self.product_id.with_context(lang=self.order_id.dest_address_id.lang or self.env.user.lang)
        date_planned = self.date_planned or self.order_id.date_planned
        return {
            # truncate to 2000 to avoid triggering index limit error
            # TODO: remove index in master?
            'name': (self.product_id.display_name or '')[:2000],
            'product_id': self.product_id.id,
            'analytic_account_id': self.account_analytic_id.id or False, # Customization on this line
            'date': date_planned,
            'date_deadline': date_planned,
            'location_id': self.order_id.partner_id.property_stock_supplier.id,
            'location_dest_id': (self.orderpoint_id and not (self.move_ids | self.move_dest_ids)) and self.orderpoint_id.location_id.id or self.order_id._get_destination_location(),
            'picking_id': picking.id,
            'partner_id': self.order_id.dest_address_id.id,
            'move_dest_ids': [(4, x) for x in self.move_dest_ids.ids],
            'state': 'draft',
            'purchase_line_id': self.id,
            'company_id': self.order_id.company_id.id,
            'price_unit': price_unit,
            'picking_type_id': self.order_id.picking_type_id.id,
            'group_id': self.order_id.group_id.id,
            'origin': self.order_id.name,
            'description_picking': product.description_pickingin or self.name,
            'propagate_cancel': self.propagate_cancel,
            'warehouse_id': self.order_id.picking_type_id.warehouse_id.id,
            'product_uom_qty': product_uom_qty,
            'product_uom': product_uom.id,
            'product_packaging_id': self.product_packaging_id.id,
            'sequence': self.sequence,
        }

    # Inherit for logging purpose, to check the base value
    # @api.depends('product_qty', 'price_unit', 'taxes_id')
    # def _compute_amount(self):
    #     _logger.info("_compute_amount")
    #     for line in self:
    #         taxes = line.taxes_id.compute_all(**line._prepare_compute_all_values())
    #         _logger.info(taxes)
    #         line.update({
    #             'price_tax': taxes['total_included'] - taxes['total_excluded'],
    #             'price_total': taxes['total_included'],
    #             'price_subtotal': taxes['total_excluded'],
    #         })


    def _prepare_compute_all_values(self):
        # _logger.info("_prepare_compute_all_values")
        '''
        Example 1: 2 items, each costing 50000 with a discount of 20000
        Initial values:

        Quantity: 2
        Price per unit: 50000
        Total: 2 * 50000 = 100000
        Discount: 20000
        Calculation:

        Discount percentage: (20000 / 100000) * 100 = 20%
        Discount per unit: (20% / 100) * 50000 = 10000
        Updated price per unit: 50000 - 10000 = 40000

        Example 2: 5 items, each costing 100000 with a discount of 20000
        Initial values:

        Quantity: 5
        Price per unit: 100000
        Total: 5 * 100000 = 500000
        Discount: 20000
        Calculation:

        Discount percentage: (20000 / 500000) * 100 = 4%
        Discount per unit: (4% / 100) * 100000 = 4000
        Updated price per unit: 100000 - 4000 = 96000
        Flow of Calculation
        In both cases, we calculate the discount percentage based on the total amount.
        Then, we calculate the discount amount per unit by applying the percentage to the price per unit.
        Finally, we subtract the discount per unit from the original price per unit to get the updated price per unit.

        This way, the discount is proportionally distributed among each unit based on their individual prices.
        The division by quantity ensures that each unit contributes to the total discount amount based on its share of the total price.
        
        
        '''
        self.ensure_one()
        
        # Retrieve the initial values without considering the discount
        values = {
            'price_unit': self.price_unit,
            'currency': self.order_id.currency_id,
            'quantity': self.product_qty,
            'product': self.product_id,
            'partner': self.order_id.partner_id,
        }

        # Subtract the discount proportionally from the base amount
        discount_val = self.discount_val
        total = values['price_unit'] * values['quantity']
        
        if values['quantity'] > 0 and total > 0:
            discount_percentage = (discount_val / total) * 100
            discount_per_unit = (discount_percentage / 100) * values['price_unit']
            
            values['price_unit'] -= discount_per_unit
        else:
            # Handle division by zero gracefully
            values['price_unit'] -= discount_val

        return values


    def _prepare_account_move_line(self, move=False):
        res = super()._prepare_account_move_line(move)
        res.update({'discount': self.discount, 'discount_val': self.discount_val})
        return res




    


