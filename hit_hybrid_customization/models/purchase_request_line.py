# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    life_of_projects = fields.Selection([
        ('3_bulan', '3 Bulan'),
        ('6_bulan', '6 Bulan'),
        ('9_bulan', '9 Bulan'),
        ('12_bulan', '12 Bulan'),
        ('15_bulan', '15 Bulan'),
        ('18_bulan', '18 Bulan'),
        ('21_bulan', '21 Bulan'),
        ('24_bulan', '24 Bulan'),
        ('27_bulan', '27 Bulan'),
        ('30_bulan', '30 Bulan'),
        ('33_bulan', '33 Bulan'),
        ('36_bulan', '36 Bulan'),
        ('39_bulan', '39 Bulan'),
        ('42_bulan', '42 Bulan'),
        ('45_bulan', '45 Bulan'),
        ('48_bulan', '48 Bulan'),
        ('51_bulan', '51 Bulan'),
        ('54_bulan', '54 Bulan'),
        ('58_bulan', '58 Bulan'),
        ('60_bulan', '60 Bulan'),
    ], string='Life of Projects')


    move_count = fields.Integer(
        string="Stock Move Count",
        related="request_id.move_count",
        readonly=True
    )

    # latest_purchase_request_allocation = fields.Many2one(
    #     string="Latest Allocation",
    #     comodel_name="purchase.request.allocation",
    #     compute="_compute_latest_allocation",
    #     store=True
    # )

    # stock_move_id = fields.Many2one(
    #     string="Stock Move",
    #     comodel_name="stock.move",
    #     ondelete="cascade",
    #     related="latest_purchase_request_allocation.stock_move_id",
    #     store=True
    # )
    
    # move_state = fields.Selection([
    #     ('draft', 'New'), ('cancel', 'Cancelled'),
    #     ('waiting', 'Waiting Another Move'),
    #     ('confirmed', 'Waiting Availability'),
    #     ('partially_available', 'Partially Available'),
    #     ('assigned', 'Available'),
    #     ('done', 'Done')], string='Moves Status',
    #     copy=False, default='draft', index=True, readonly=True,
    #     related='stock_move_id.state',
    #     help="*Following State of the related stock move\n")

    # stock_move_number = fields.Integer('Stock Move Number', related='stock_move_id.id')

    site_id = fields.Many2one('md.site', string='Site', related='request_id.site_id', store=True)


    @api.constrains('analytic_account_id')
    def _constrains_analytic_account_id(self):
        for record in self:
            if record.product_id and not record.analytic_account_id:
                raise ValidationError(_('The analytic account requires mandatory input.'))


    # @api.depends('purchase_request_allocation_ids.write_date')
    # def _compute_latest_allocation(self):
    #     for record in self:
    #         latest_allocation = record.purchase_request_allocation_ids.sorted(
    #             key=lambda r: r.write_date, reverse=True
    #         )[:1]
    #         if latest_allocation:
    #             record.latest_purchase_request_allocation = latest_allocation[0]
    #         else:
    #             record.latest_purchase_request_allocation = False


    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.analytic_account_id = False
            site_id = self.site_id.id
            if site_id:
                domain = [("site_id", "=", site_id)]
                return {"domain": {"analytic_account_id": domain}}
            else:
                return {"domain": {"analytic_account_id": [("site_id", "=", False)]}}
        else:
            self.analytic_account_id = False
            return {"domain": {"analytic_account_id": [("site_id", "=", False)]}}



class PurchaseRequestAllocation(models.Model):
    _inherit = "purchase.request.allocation"
    

    stock_move_number = fields.Integer('Stock Move Number', related='stock_move_id.id')