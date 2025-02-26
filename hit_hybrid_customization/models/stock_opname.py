from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class HITStockOpname(models.Model):
    _name = 'hit.stock.opname'
    _description = 'HIT Stock Opname'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char('Nomer Dokumen')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='draft', string='State')
    date = fields.Datetime('Date')
    backdate_inventory = fields.Datetime('Backdate Inventory')
    accounting_date = fields.Date('Accounting Date')
    location_id = fields.Many2one('stock.location', string='Location')
    user_id = fields.Many2one('res.users', string='User')
    opname_line_ids = fields.One2many('hit.stock.opname.line', 'opname_id', string='Opname Line')

    def button_populate(self):
        '''When creating a quant, it initially sets the Stock on Hand (SoH) to zero instead of the counted quantity.
        Therefore, we need to execute this process twice to fill in the counted quantity.'''
        for line in self.opname_line_ids:
            if line.quant_id:
                line.quant_id.inventory_quantity = 0
                line.quant_id.inventory_diff_quantity = 0
                line.quant_id.inventory_quantity_set = False
                line.quant_id.accounting_date = False
                line.quant_id.backdate_inventory = False
        self.button_count()
    
    def button_count(self):
        for line in self.opname_line_ids:
            # Find the corresponding stock.quant record
            quant = self.env['stock.quant'].search([
                ('product_id', '=', line.product_id.id),
                ('location_id', '=', self.location_id.id)
            ], limit=1)

            if quant:
                # Update the counted quantity
                quant.write({
                    'inventory_quantity': line.inventory_quantity,
                    'accounting_date': self.accounting_date,
                    'backdate_inventory': self.backdate_inventory
                })
            else:
                # Create a new stock.quant record
                quant = self.env['stock.quant'].create({
                    'product_id': line.product_id.id,
                    'location_id': self.location_id.id,
                    'inventory_quantity': line.inventory_quantity,
                    'lot_id': line.lot_id.id,
                    'accounting_date': self.accounting_date,
                    'backdate_inventory': self.backdate_inventory,
                })
            # Store the quant in the line for later use
            line.quant_id = quant

    def button_apply(self):
        for line in self.opname_line_ids:
            if line.quant_id:
                line.quant_id._apply_inventory()
        


class HITStockOpname(models.Model):
    _name = 'hit.stock.opname.line'
    _description = 'HIT Stock Opname'

    opname_id = fields.Many2one('hit.stock.opname', string='Opname')
    product_id = fields.Many2one('product.product', string='Product')
    lot_id = fields.Many2one('stock.production.lot', string='Lot/Serial Number')
    uom_id = fields.Many2one('uom.uom', string='UoM')
    quantity = fields.Float('SoH', compute='_compute_quantity', store=False)
    inventory_quantity = fields.Float('Opname Qty')
    inventory_diff_quantity = fields.Float('Inventory Diff Quantity')
    quant_id = fields.Many2one('stock.quant', string='Quant')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id

    @api.depends('product_id', 'lot_id', 'opname_id.location_id')
    def _compute_quantity(self):
        for record in self:
            if record.product_id:
                available_quantity = 0
                record.uom_id = record.product_id.uom_id.id
                if record.lot_id:
                    available_quantity = self.env['stock.quant']._get_available_quantity(
                        product_id=record.product_id,
                        location_id=record.opname_id.location_id,
                        lot_id=record.lot_id
                    )
                else:
                    available_quantity = self.env['stock.quant']._get_available_quantity(
                        product_id=record.product_id,
                        location_id=record.opname_id.location_id
                    )
                # Set the quantity field
                record.quantity = available_quantity

        

    