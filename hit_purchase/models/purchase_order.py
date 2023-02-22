# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    complete_gr = fields.Boolean('Complete GR')
    create_by_pr = fields.Boolean('Create by PR')
    rfq = fields.Char('RFQ')
    purchase_request_id = fields.Many2one(
        'purchase.request', string='Purchase Request')

    @api.onchange('purchase_request_id')
    def _onchange_purchase_order_items(self):
        for record in self:
            if record.purchase_request_id:
                record['order_line'] = [(5, 0, 0)]
                for line in record.purchase_request_id.line_ids:
                    record['order_line'] = [(0, 0, {'order_id': record.id,
                                                    'product_template_id': line.product_id.id,
                                                    'name': line.name,
                                                    'product_qty': line.purchased_qty,
                                                    'product_uom': line.product_uom_id.id,
                                                    'price_unit': line.estimated_cost
                                                    })]


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    schedule_date = fields.Datetime(
        'Schedule Date', related='order_id.effective_date')
    status = fields.Char('Purchase Status', compute='_compute_status')

    @api.depends('schedule_date', 'date_planned')
    def _compute_status(self):
        for record in self:
            result = ""
            if record.date_planned and record.schedule_date:
                count = record.date_planned - record.schedule_date
                if count.days == 0:
                    result = "Ontime"
                elif count.days < 0:
                    result = "Early"
                else:
                    result = "Delay"
            record.status = result
