from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = 'Transfer'

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic Account')
    reservation_id = fields.Many2one(
        comodel_name='reservation', string='Reservation')
    # approval_list = fields.One2many(
    #     comodel_name='approval_list', string='Approval List')
    cek_actual_price = fields.Float(string='Cek Actual Price', compute="_compute_actual_price")
    cek_total_demand = fields.Float(string='Cek Total Demand')
    create_by_reservation = fields.Boolean(string='Create by Reservation')
    create_pr = fields.Boolean(string='Create PR')
    equipment_id = fields.Many2one(
        comodel_name='maintenance.equipment', string='Equipment', related='reservation_id.equipment')
    equipment_type = fields.Char(
        string='Equipment Type', related='equipment_id.eqp_type')
    gran = fields.Float(string='Gran')
    grand_total = fields.Float(string='Actual Cost')
    done_date = fields.Date(string='WO Done Date',
                            related='reservation_id.done_date')
    operation_type = fields.Char(
        string='Operation Types', related='picking_type_id.display_name')
    outstanding_price = fields.Float(string='Outstanding Cost')
    pr = fields.Many2one(comodel_name='purchase.request',
                         string='Purchase Request')
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
        comodel_name='maintenance.request', string='Work Order', related='reservation_id.work_order')

    @api.onchange('reservation_id')
    def _onchange_stock_picking_items(self):
        for record in self:
            if record.reservation_id:
                record['move_ids_without_package'] = [(5, 0, 0)]
                for line in record.reservation_id.reservation_line_ids:
                    record['move_ids_without_package'] = [(0, 0, {'picking_id': record.id,
                                                                  'product_id': line.product_id.id,
                                                                  'product_uom_qty': line.quantity,
                                                                  'product_uom': line.uom.id,
                                                                  'location_id': record.location_id,
                                                                  'location_dest_id': record.location_dest_id
                                                                  })]
    @api.depends('move_ids_without_package')
    def _compute_actual_price(self):
            for record in self:
                total = 0
                for line in record.move_ids_without_package:
                    total += line.total_price
                record['cek_actual_price'] = total