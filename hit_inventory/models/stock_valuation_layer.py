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
    temporary_total_value = fields.Monetary(
        string='Actual Value', compute='_compute_temporary_total_value')

    @api.depends('value', 'reservation_type', 'operation_type')
    def _compute_temporary_total_value(self):
        for record in self:
            absolute_value = 0
            actual_cost = 0
            total_value = record.value
            if total_value < 0:
                absolute_value = -1 * total_value
            else:
                absolute_value = -1 * total_value
            absolute_value = absolute_value
            if record.reservation_type == '2':
                actual_cost = absolute_value
            elif record.reservation_type == '1':
                if record.operation_type.name == 'Inventory Issued':
                    actual_cost = absolute_value
                else:
                    actual_cost = 0
            actual_cost = actual_cost
            record.write({'temporary_total_value': actual_cost})
            record.write({'filter_value': actual_cost})
