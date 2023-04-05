# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    @api.onchange('x_studio_asset')
    def _onchange_account_asset(self):
        for record in self:
            asset_analytic_account = record.x_studio_asset.account_analytic_id
            asset_analytic_site = asset_analytic_account.x_studio_site if asset_analytic_account else None
            record.x_studio_analytic_account = asset_analytic_account.id if asset_analytic_account else None
            record.x_studio_warehouse = asset_analytic_site.id if asset_analytic_site else None
            record.x_studio_locations = asset_analytic_site.lot_stock_id if asset_analytic_site else None
