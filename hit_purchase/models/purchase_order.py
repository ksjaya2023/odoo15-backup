# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    complete_gr = fields.Boolean('Complete GR')
    create_by_pr = fields.Boolean('Create by PR')
    rfq = fields.Char('RFQ')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    schedule_date = fields.Date('Schedule Date')
    status = fields.Char('Purchase Status')
