# -*- coding: utf-8 -*-

from odoo import models, fields, api


class reservation(models.Model):
    _name = 'reservation'
    _description = 'reservation'

    active = fields.Boolean(string='Active', store=True)
    color = fields.Integer(string='Color')
    currency_id = fields.Many2many(
        comodel_name='res.currency', string='Currency')
    name = fields.Char(string='Name')
    analytic_account = fields.Many2many(
        comodel_name='account.analytic.account', string='Analytic Account')
    company_id = fields.Many2many(comodel_name='res.company', string='Company')
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
    kanban_state = fields.Selection(string='Kanban State', selection=[(
        'normal', 'In Progress'), ('done', 'Ready'), ('blocked', 'Blocked')])
    notes = fields.Html(string='Notes')
    email = fields.Char(string='Email')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Contact')
    partner_phone = fields.Char(string='Phone')
    pr_number = fields.Many2one(
        comodel_name='purchase.request', string='PR Number')
    reservation_type = fields.Selection(string='Reservation Type', selection=[
                                        ('1', 'Stock'), ('2', 'Non Stock')])
    user_id = fields.Many2one(comodel_name='res.users', string='Responsible')
    value = fields.Float(string='Grand Total', readonly=True)
    work_order = fields.Many2one(
        comodel_name='maintenance.request', string='Work Order')
    reservation_line_count = fields.Integer(string='Reservation Count')
    reservation_stock_picking_count = fields.Integer(string='Issued')
