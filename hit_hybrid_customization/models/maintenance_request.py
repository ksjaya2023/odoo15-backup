
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    wo_done_date_time = fields.Datetime(
        compute='_compute_wo_done_date_time', string='Complete Time')

    @api.depends('stage_id.name')
    def _compute_wo_done_date_time(self):
        for record in self:
            if record.stage_id.name == 'Done':
                record.wo_done_date_time = fields.Datetime.now()
            else:
                record.wo_done_date_time = None

    @api.onchange('wo_done_date_time', 'schedule_date')
    def _onchange_wo_done_date_time(self):
        for record in self:
            if record.schedule_date and record.wo_done_date_time:
                diff = record.wo_done_date_time - record.schedule_date
                result = abs(diff)
                record.duration = result.total_seconds() / 3600

    # @api.onchange('x_studio_asset')
    # def _onchange_account_asset(self):
    #     for record in self:
    #         if record.x_studio_asset:
    #             asset_analytic_account = record.x_studio_asset.account_analytic_id
    #             asset_analytic_site = asset_analytic_account.x_studio_site
    #             if asset_analytic_account:
    #                 record.x_studio_analytic_account = asset_analytic_account.id
    #             if not asset_analytic_account:
    #                 record.x_studio_analytic_account = None
    #             if asset_analytic_site:
    #                 record.x_studio_warehouse = asset_analytic_site.id
    #             if not asset_analytic_site:
    #                 record.x_studio_warehouse = None
    #                 record.x_studio_locations = None
