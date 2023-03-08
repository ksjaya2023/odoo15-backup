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
        'maintenance.equipment', string='Equipment', related='reservation_id.equipment')
    return_request_ids = fields.One2many(
        'return.request.line', 'return_request_id', string='Return Request')
    transfer_id = fields.Many2one('stock.picking', string='Transfer')
    work_order_id = fields.Many2one(
        'maintenance.request', string='Work Order', related='reservation_id.work_order')
    create_gi = fields.Boolean('Create GI')

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

    def create_returns(self):
        import ipdb

        rec_opr_type = 0
        opr_type = self.env['stock.picking.type'].search(
            [('name', 'ilike', 'Returns')])
        for row_opr_type in opr_type:
            rec_opr_type = row_opr_type.id

        rec_src_loc = 0
        src_loc = self.env['stock.location'].search(
            [('name', 'ilike', 'Stock')])
        for row_src_loc in src_loc:
            rec_src_loc = row_src_loc.id

        dest_loc_id = 0
        dest_loc = self.env['stock.location'].search(
            [('name', 'ilike', 'Stock'), ('location_id', 'ilike', 'WH')])
        for row_dest_loc in dest_loc:
            dest_loc_id = row_dest_loc.id

        if rec_opr_type:
            if rec_src_loc:
                return_doc = self.env['stock.picking'].create({'location_dest_id': dest_loc_id,
                                                               'location_id': dest_loc_id,
                                                               'picking_type_id': rec_opr_type,
                                                               'move_type': 'direct',
                                                               'return_request': self.id,
                                                               'reservation_id': self.reservation_id.id,
                                                               'equipment_id': self.equipment_id.id,
                                                               'work_order': self.work_order_id.id
                                                               })
                if return_doc:
                    return_id = 0
                    for row_return in return_doc:
                        ipdb.set_trace()
                        row_return.return_request = row_return.id
                        return_id = row_return.id
                    for item in self.return_request_ids:
                        self.env['stock.move'].create({'product_id': item.product_id.id,
                                                       'product_uom_qty': item.quantity,
                                                       'picking_id': return_id,
                                                       'name': item.product_id.name,
                                                       'product_uom': item.uom_id.id,
                                                       'location_id': dest_loc_id,
                                                       'location_dest_id': rec_src_loc
                                                       })
                    return self.write({
                        "create_gi": True,
                        "transfer_id": return_id,
                    })

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            seq = self.env['ir.sequence'].next_by_code('return.request.seq')
            val['name'] = seq
            create_data = super(ReturnRequest, self).create(vals)
            create_data.create_returns()
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
    description = fields.Char('Description', related='product_id.name')
