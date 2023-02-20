# Author: Siti Mayna
from odoo import _, api, fields, models


class ReturnRequest(models.Model):
    _name = 'return.request'
    _description = 'Return Request'

    name = fields.Char('Name', default="Draft")
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer('Sequence')
    reservation_id = fields.Many2one(
        comodel_name='reservation', string='Reservation')
    equipment_id = fields.Many2one(
        'maintenance.equipment', string='Equipment', related='reservation_id.equipment')  # related
    return_request_ids = fields.One2many(
        'return.request.line', 'return_request_id', string='Return Request')
    return_document_id = fields.Many2one(
        'return.request', string='Return Document')  # related
    transfer_id = fields.Many2one('stock.picking', string='Transfer')
    work_order_id = fields.Many2one(
        'maintenance.request', string='Work Order', related='reservation_id.work_order')  # related

    @api.onchange('reservation_id')
    def _onchange_return_request_items(self):
        for record in self:
            if record.reservation_id:
                record['return_request_ids'] = [(5, 0, 0)]
                for line in record.reservation_id.reservation_line_ids:
                    record['return_request_ids'] = [(0, 0, {'product_id': line.product_id.id,
                                                            'quantity': line.quantity,
                                                            'return_request_id': record.id,
                                                            'uom_id': line.uom.id
                                                            })]

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('return.request.seq')
        vals['name'] = seq
        create_data = super(ReturnRequest, self).create(vals)
        return create_data


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
    description = fields.Char('Description')
