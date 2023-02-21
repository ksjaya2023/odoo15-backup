from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'
    _description = 'Stock Move'

    currency_id = fields.Many2one(
        comodel_name='res.currency', string='Currency')
    reservation_id = fields.Many2one(
        comodel_name='reservation', string='Reservation id', related='picking_id.reservation_id')
    binlocation = fields.Many2one(
        comodel_name='bin.location', string='Bin Location', related='product_tmpl_id.bin_location')
    demand_price = fields.Float(string='Demand Price')
    equipment = fields.Many2one(
        comodel_name='maintenance.equipment', string='Equipment', related='picking_id.equipment_id')
    equipment_type = fields.Char(
        string='Equipment Type', related='picking_id.equipment_type')
    part_number = fields.Char(string='Part Number',
                              related='product_tmpl_id.part_number')
    reservation_description = fields.Char(
        string='Reservation Description', related='picking_id.reservation_id.description')
    reservation_type = fields.Selection(
        string='Reservation Type', related='picking_id.reservation_id.reservation_type')
    standard_price = fields.Float(
        string='Cost', related='product_id.standard_price')
    stock_code = fields.Char(
        string='Stock Code', related='product_tmpl_id.default_code')
    total_price = fields.Float(string='Total Price')
    allocation_ids = fields.One2many(
        'purchase.request.allocation', 'stock_move_id', string='Allocation')
