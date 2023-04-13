# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    @api.onchange('x_studio_asset')
    def _onchange_account_asset(self):
        for record in self:
            asset_analytic_type = record.x_studio_asset.x_studio_asset_types
            asset_analytic_account = record.x_studio_asset.account_analytic_id
            asset_analytic_site = asset_analytic_account.x_studio_site if asset_analytic_account else None
            record.x_studio_analytic_account = asset_analytic_account.id if asset_analytic_account else None
            record.x_studio_warehouse = asset_analytic_site.id if asset_analytic_site else None
            record.x_studio_locations = asset_analytic_site.lot_stock_id if asset_analytic_site else None
            record.x_studio_many2one_class = asset_analytic_type.id if asset_analytic_type else None
            # Fill vendor datain equipment using partner_id in asset if exist
            asset_related_purchase = record.x_studio_asset.original_move_line_ids.filtered(
                lambda line: line.partner_id)
            if asset_related_purchase:
                record.partner_id = asset_related_purchase[0].partner_id.id
            else:
                record.partner_id = None

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for record in self:
            record.x_studio_department = record.employee_id.department_id.id
