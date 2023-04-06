
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    report_id = fields.Many2one('ir.actions.report', string="Report")

    def alter_print_quotation(self):
        self.write({'state': "sent"})
        return self.env.ref('studio_customization.studio_report_docume_1a8d804f-45d7-4e0a-bea8-f1edbef0d495')
        # return self.env.ref('studio_customization.studio_report_docume_1a8d804f-45d7-4e0a-bea8-f1edbef0d495').report_action(self)
