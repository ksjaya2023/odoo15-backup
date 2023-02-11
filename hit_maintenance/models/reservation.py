# -*- coding: utf-8 -*-

from odoo import models, fields, api

_STATUS = [
    ("installed", "Installed"),
    ("not_installed", "Not Installed"),
    ("return", "Return")
]

_STATUS_1 = [
    ("installed", "Installed"),
    ("not_installed", "Not Installed"),
    ("return", "Return"),
    ("finish", "Finish")
]

_KANBAN_STATE = [
    ('normal', 'In Progress'),
    ('done', 'Ready'),
    ('blocked', 'Blocked')
]

_RESERVATION_STATUS = [
    ('new', 'New'),
    ('approve', 'Approve'),
    ('in_progress', 'In Progress'),
    ('done', 'Done'),
    ('cancel', 'Cancel')
]


class Reservation(models.Model):
    _name = 'reservation'
    _description = 'reservation'

    name = fields.Char('Name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')
    priority = fields.Boolean(string='High Priority')
    color = fields.Char(string='Color Index')
    reservation_line_ids = fields.One2many(
        comodel_name='reservation.line', inverse_name='reservation_id', string='Reservation Line Item')
    currency_id = fields.Many2one(
        comodel_name='res.currency', string='Currency')
    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic Account')
    company_id = fields.Many2one(comodel_name='res.company', string='Company')
    create_by_wo = fields.Boolean(string='Creat by WO')
    create_gi = fields.Boolean(string='Creat GI')
    create_pr = fields.Boolean(string='Creat PR')
    date = fields.Date(string='Date')
    description = fields.Char(string='Description')
    done_date = fields.Date(string='Done Date', readonly=True)
    equipment = fields.Many2one(
        comodel_name='maintenance.equipment', string='Equipment', readonly=True)
    gi = fields.Many2one(comodel_name='stock.picking', string='GI Number')
    image = fields.Binary(string='Image')
    kanban_state = fields.Selection(
        string='Kanban State', selection=_KANBAN_STATE)
    notes = fields.Html(string='Notes')
    partner_email = fields.Char(string='Email')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Contact')
    partner_phone = fields.Char(string='Phone')
    # pr_number = fields.Many2one(
    #     comodel_name='purchase.request', string='PR Number')
    reservation_type = fields.Selection(string='Reservation Type', selection=[
                                        ('1', 'Stock'), ('2', 'Non Stock')])
    status = fields.Selection(
        string='Status Bar', selection=_RESERVATION_STATUS)
    user_id = fields.Many2one(comodel_name='res.users', string='Responsible')
    return_request_id = fields.Many2one(
        'return.request', string='Return Request')
    reservation_stage_id = fields.Many2one(
        'reservation.stage', string='Reservation Stage')
    reservation_tag_ids = fields.Many2many(
        'reservation.tag', string='Reservation Tag')
    value = fields.Float(string='Grand Total', readonly=True)
    work_order = fields.Many2one(
        comodel_name='maintenance.request', string='Work Order')
    reservation_line_count = fields.Integer(
        string='Reservation Count')  # compute
    reservation_stock_picking_count = fields.Integer(
        string='Issued')  # compute
    return_request_id = fields.Many2one(
        'return.request', string='Return Request')
    return_request_ids = fields.One2many(
        'return.request', 'reservation_id', string='Return Requests')


class ReservationLine(models.Model):
    _name = 'reservation.line'
    _description = 'reservation line'

    name = fields.Char('Name')
    currency_id = fields.Many2one('res.currency', string='Currency')
    reservation_id = fields.Many2one(
        comodel_name='reservation', string='Reservation ID')
    date = fields.Date(string='Date')
    date_install = fields.Date(string='Date Install')
    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic Account')
    product_id = fields.Many2one(
        comodel_name='product.product', string='Products')
    # price = fields.Float(string='Price', tracking=True,
    #                      related=product_id.price)
    # standard_price = fields.Float(
    #     string='Standard Price', tracking=True, related=product_id.standard_price)
    product = fields.Char(string='Product')
    product_name = fields.Char(string='Product Name')
    quantity = fields.Integer(string='Quantity')
    # quantity_on_hand = fields.Float(
    #     string='Quantity on Hand', tracking=True, related=product_id.qty_available)
    reqmt_date = fields.Date(string='Requirement Date')
    sequence = fields.Integer(string='Sequence')
    status = fields.Selection(string='', selection=_STATUS)
    status_1 = fields.Selection(string='', selection=_STATUS_1)
    total_price = fields.Float(string='Est. Total Price')
    # uom = fields.Many2one(comodel_name='uom.uom',
    #                       string='UoM', related=product_id.uom_id)
    work_order_related = fields.Many2one(
        comodel_name='maintenance.request', string='Work Order Related')
