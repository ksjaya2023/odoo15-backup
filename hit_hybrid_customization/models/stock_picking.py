# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.depends('state', 'x_studio_operation_type_name')
    def _compute_show_validate(self):
        for picking in self:
            super(StockPicking, picking)._compute_show_validate()
            if picking.state == 'assigned' and picking.x_studio_operation_type_name == 'Return to Vendor' and picking.x_studio_still_in_approval == True:
                picking.show_validate = False
