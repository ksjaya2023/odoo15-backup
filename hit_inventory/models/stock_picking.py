from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = 'Transfer'

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic Account')
    # approval_list = fields.One2many(
    #     comodel_name='approval_list', string='Approval List')
    cek_actual_price = fields.Float(string='Cek Actual Price')
    cek_total_demand = fields.Float(string='Cek Total Demand')
    create_by_reservation = fields.Boolean(string='Create by Reservation')
    create_pr = fields.Boolean(string='Create PR')
    done_date = fields.Date(string='WO Done Date')
    equipment_id = fields.Many2one(
        comodel_name='maintenance.equipment', string='Equipment')
    equipment_type = fields.Char(string='Equipment Type')
    gran = fields.Float(string='Gran')
    grand_total = fields.Float(string='Actual Cost')
    reservation_id = fields.Many2one(
        comodel_name='reservation', string='Reservation')
    operation_type = fields.Char(string='Operation Type')
    outstanding_price = fields.Float(string='Outstanding Cost')
    # pr = fields.Many2one(comodel_name='purchase.request',
    #                      string='Purchase Request')
    receive_date = fields.Datetime(string='Receive Date')
    stock_picking_type = fields.Selection(string='New Related Field',
                                          selection=[('incoming', 'Receipt'), ('outgoing', 'Delivery'),
                                                     ('internal', 'Internal Transfer'), ('mrp_operation', 'Manufacturing')])
    reservation_item = fields.One2many(
        comodel_name='reservation.line', inverse_name='stock_picking_id', string='Reservation Item')
    return_request = fields.Many2one(
        comodel_name='return.request', string='Return Request')
    total_demand = fields.Float(string='Total Demand')
    work_order = fields.Many2one(
        comodel_name='maintenance.request', string='Work Order')
