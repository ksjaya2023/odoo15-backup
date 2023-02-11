# Author: Siti Mayna
from odoo import _, api, fields, models


class ReturnRequest(models.Model):
    _name = 'return.request'
    _description = 'Return Request'

    name = fields.Char('Name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer('Sequence')
    reservation_id = fields.Many2one(
        comodel_name='reservation', string='Reservation')
    equipment_id = fields.Many2one(
        'maintenance.equipment', string='Equipment')  # related
    return_request_ids = fields.One2many(
        'return.request.line', 'return_request_id', string='Return Request')
    return_document_id = fields.Many2one(
        'return.request', string='Return Document')  # related
    transfer_id = fields.Many2one('stock.picking', string='Transfer')
    work_order_id = fields.Many2one(
        'maintenance.request', string='Work Order')  # related


class ReturnRequestLine(models.Model):
    _name = 'return.request.line'
    _description = 'Return Request Line'

    name = fields.Char('Name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer('Sequence')
    return_request_id = fields.Many2one(
        'return.request', string='Return Request')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float('Quantity')
    uom_id = fields.Many2one('uom.uom', string='UoM')
