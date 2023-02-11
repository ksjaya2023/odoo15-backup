from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # purchase_request_code = fields.Many2one(
    #     'purchase.request', string='Request Reference')
    purchase_request_lines = fields.Many2many(
        readonly=False,
        # store=True
    )
    purchase_request_code = fields.Many2one(
        string='Request Reference',
        store=True,
        related="purchase_request_lines.request_id")

    # # somehow we can create it
    # def create(self, vals):
    #     return super(PurchaseOrderLine, self).create(vals)
