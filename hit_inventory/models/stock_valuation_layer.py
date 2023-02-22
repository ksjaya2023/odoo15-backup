from odoo import models, fields, api


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'
    _description = 'Stock Valuation Layer'

    equipment = fields.Many2one(
        comodel_name='maintenance.equipment', string='Equipment', related='stock_move_id.equipment')
    equipment_type = fields.Char(
        string='Equipment Type', related='stock_move_id.equipment_type')
    filter_value = fields.Float(string='Filter Value')
    monetary_field_3bOND = fields.Monetary(string='New Monetary')
    operation_type = fields.Many2one(
        comodel_name='stock.picking.type', string='Operation Type', related='stock_move_id.picking_type_id')
    reservation_description = fields.Char(
        string='Reservation Description', related='stock_move_id.reservation_description')
    reservation_type = fields.Selection(
        string='Reservation Type', related='stock_move_id.reservation_type')
    temporary_total_value = fields.Monetary(string='Actual Value')
