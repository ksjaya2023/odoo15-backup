# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    purchase_type = fields.Selection([
        ('purchase_request', 'Purchase Request'),
        ('asset_request', 'Asset Request')
    ], string='purchase_type')

    site_id = fields.Many2one('stock.warehouse', string='Site')

    @api.onchange('purchase_type')
    def _onchange_purchase_type(self):
        for record in self:
            _logger.info(record.picking_type_id)
            if record.purchase_type and record.picking_type_id:
                record.site_id = record.picking_type_id.warehouse_id.id