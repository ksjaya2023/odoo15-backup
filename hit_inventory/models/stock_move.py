from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'
    _description = 'Stock Move'

    currency_id = fields.Many2one(
        comodel_name='res.currency', string='Currency')
    binlocation = fields.Many2one(
        comodel_name='bin.location', string='Bin Location')
    demand_price = fields.Float(string='Demand Price')
    equipment = fields.Many2one(
        comodel_name='maintenance.equipment', string='Equipment')
    equipment_type = fields.Char(string='Equipment Type')
    part_number = fields.Char(string='Part Number')
    related_field_Bvv6h = fields.Float(string='New Related Field')
    reservation_description = fields.Char(string='Reservation Description')
    # reservation_id = fields.Many2one(
    #     comodel_name='x_reservation', string='Reservation id')
    reservation_type = fields.Selection(string='Reservation Type',
                                        selection=[('1', 'Stock'), ('2', 'Non Stock')])
    standard_price = fields.Float(string='Cost')
    stock_code = fields.Char(string='Stock Code')
    total_price = fields.Float(string='Total Price')
    allocation_ids = fields.One2many(
        'purchase.request.allocation', 'stock_move_id', string='Allocation')
