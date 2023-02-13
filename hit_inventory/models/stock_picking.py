from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = 'Transfer'

    analytic_account = fields.Many2one(comodel_name='account.analytic.account', string='Analytic Account')
    # approval_list = fields.One2many(
    #     comodel_name='approval_list', string='Approval List')
    cek_actual_price = fields.Float(string='Cek Actual Price')
    cek_total_demand= fields.Float(string='Cek Total Demand')
    create_by_reservation= fields.Boolean(string='Create by Reservation')
    create_pr= fields.Boolean(string='Create PR')
    done_date= fields.Date(string='WO Done Date')
    equipment= fields.Many2one(comodel_name='maintenance.equipment', string='Equipment')
    equipment_type= fields.Char(string='Equipment Type')
    float_field_cgZkn= fields.Float(string='New Decimal')
    gran= fields.Float(string='Gran')
    grand_total= fields.Float(string='Actual Cost')
    # many2one_reservation= fields.Many2one(comodel_name='reservation', string='Reservation')
    operation_type= fields.Char(string='Operation Type')
    outstanding_price= fields.Float(string='Outstanding Cost')
    pr= fields.Many2one(comodel_name='purchase.request', string='Purchase Request')
    receive_date= fields.Datetime(string='Receive Date')
    related_field_UKKJ4= fields.Boolean(string='New Related Field')
    related_field_akL4t = fields.Selection(string='New Related Field', 
                                            selection=[('incoming', 'Receipt'), ('outgoing', 'Delivery'),
                                                        ('internal', 'Internal Transfer'), ('mrp_operation', 'Manufacturing')])
    # reservation_item= fields.One2many(
    #     comodel_name='reservation_line_a7ec4', string='Reservation Item')
    # return_request= fields.Many2one(comodel_name='return_request', string='Return Request')
    # still_in_approval= fields.Boolean(string='still in approval')
    total_demand= fields.Float(string='Total Demand')
    work_order= fields.Many2one(comodel_name='maintenance.request', string='Work Order')