from odoo import models, fields, api


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'
    _description = 'Purchase Request'

    create_by_issue = fields.Boolean('Create by Issue')
    create_by_reservasi = fields.Boolean('Create by Reservasi')
    create_rfq = fields.Boolean('Create RFQ')
    document_name = fields.Char('Document Name')
    purchase_order_id = fields.Many2one(
        comodel_name='purchase.order', string='Purchase Order')
    reservation_id = fields.Many2one(
        comodel_name='reservation', string='Reservation')
    purchase_type = fields.Selection(string='Purchase Type',
                                     selection=[('Purchase Request', 'Purchase Request'), ('Asset Request', 'Asset Request')])
    request_number = fields.Char('Request Number')
    request_type = fields.Selection(string='Request Type',
                                    selection=[('Stock', 'Stock'), ('Non Stock', 'Non Stock'), ('General', 'General')])
    rfq = fields.Many2one(comodel_name='purchase.order', string='RFQ')

    @api.onchange('reservation_id')
    def _onchange_purchase_request_items(self):
        for record in self:
            if record.reservation_id:
                record['line_ids'] = [(5, 0, 0)]
                for line in record.reservation_id.reservation_line_ids:
                    record['line_ids'] = [(0, 0, {'request_id': record.id,
                                                  'product_id': line.product_id.id,
                                                  'product_qty': line.quantity,
                                                  'product_uom_id': line.uom.id,
                                                  'estimated_cost': line.price
                                                  })]
