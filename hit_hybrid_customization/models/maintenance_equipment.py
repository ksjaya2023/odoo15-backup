# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"


    @api.onchange("x_studio_asset")
    def _onchange_account_asset(self):
        """
        This method is triggered when the 'x_studio_asset' field changes. It updates several fields
        in the maintenance equipment model based on the related asset's properties. Specifically, it:
        - Sets the analytic account, warehouse, and location fields based on the asset's analytic account and site.
        - Sets the class field based on the asset's type.
        - Updates the vendor information in the equipment using the partner ID from the asset's original move line, if available.
        - x_studio_site is a many2one field related to stock.warehouse. 
        - It might be confusing due to the existence of site master data.
        - Both fields exist; try to locate the field in the technical menu under 'field'.
        """
        for record in self:
            asset_analytic_type = record.x_studio_asset.x_studio_asset_types
            asset_analytic_account = record.x_studio_asset.account_analytic_id
            asset_analytic_site = (
                asset_analytic_account.x_studio_site if asset_analytic_account else None
            )
            record.x_studio_analytic_account = (
                asset_analytic_account.id if asset_analytic_account else None
            )
            record.x_studio_warehouse = (
                asset_analytic_site.id if asset_analytic_site else None
            )
            record.x_studio_locations = (
                asset_analytic_site.lot_stock_id if asset_analytic_site else None
            )
            record.x_studio_many2one_class = (
                asset_analytic_type.id if asset_analytic_type else None
            )
            # Fill vendor datain equipment using partner_id in asset if exist
            asset_related_purchase = (
                record.x_studio_asset.original_move_line_ids.filtered(
                    lambda line: line.partner_id
                )
            )
            if asset_related_purchase:
                record.partner_id = asset_related_purchase[0].partner_id.id
            else:
                record.partner_id = None


    @api.onchange("employee_id")
    def _onchange_employee_id(self):
        for record in self:
            record.x_studio_department = record.employee_id.department_id.id


    def name_get(self):
        result = []
        for record in self:
            if record.x_studio_equipment_name:
                result.append((record.id, record.x_studio_equipment_name))
            else:
                result.append((record.id, record.name))
        return result


    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if operator == 'ilike':
            args = ['|',
                    ('name', 'ilike', name),
                    ('x_studio_equipment_name', 'ilike', name)]
            return self._search(args, limit=limit, access_rights_uid=name_get_uid)

        return super()._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
