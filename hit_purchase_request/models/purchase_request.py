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
