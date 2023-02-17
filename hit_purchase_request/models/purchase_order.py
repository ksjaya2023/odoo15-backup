# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    _description = 'Purchase Order'

    complete_gr = fields.Boolean(string='Complete GR')
    create_by_pr = fields.Boolean(string='Create by PR')
    many2one_pr = fields.Many2one(comodel_name='purchase.request', string='Purchase Request')
    # pr_line = fields.One2many()
    rfq = fields.Char(string='RFQ')
    # still_in_approval = fields.Boolean(string='still in approval')



class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    schedule_date = fields.Date('Schedule Date')
    status = fields.Char('Purchase Status')
