# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    show_validate = fields.Boolean(compute='_compute_show_validate')

    @api.depends('state', 'x_studio_operation_type_name')
    def _compute_show_validate(self):
        for picking in self:
            if not (picking.immediate_transfer) and picking.state == 'draft':
                picking.show_validate = False
            elif picking.state not in ('draft', 'waiting', 'confirmed', 'assigned') and picking.x_studio_operation_type_name != 'Return to Vendor':
                picking.show_validate = False
            elif picking.state in ('draft', 'waiting', 'confirmed', 'assigned') and picking.x_studio_operation_type_name != 'Return to Vendor':
                picking.show_validate = True
            elif picking.state != 'assigned' and picking.x_studio_operation_type_name == 'Return to Vendor':
                picking.show_validate = False
