from odoo import models, fields, api


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'
    _description = 'Stock Valuation Layer'

    equipment = fields.Many2one(
        comodel_name='maintenance.equipment', string='Equipment')
    equipment_type = fields.Char(string='Equipment Type')
    filter_value = fields.Float(string='Filter Value')
    monetary_field_3bOND = fields.Monetary(string='New Monetary')
    operation_type = fields.Many2one(
        comodel_name='stock.picking.type', string='Operation Type')
    reservation_description = fields.Char(string='Reservation Description')
    reservation_type = fields.Selection(string='Reservation Type',
                                          selection=[('1', 'Stock'), ('2', 'Non Stock')])
    temporary_total_value = fields.Monetary(string='Actual Value')
