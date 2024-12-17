
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    wo_done_date_time = fields.Datetime(
        compute='_compute_wo_done_date_time', string='Complete Time')
    inspection_id = fields.Many2one(
        string='Inspection',
        comodel_name='hit.condition.monitoring'
    )


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


    @api.onchange('inspection_id')
    def _onchange_inspection_id(self):
        if self.inspection_id:
            if self.x_studio_work_order_type != 'Perbaikan':
                self.x_studio_attachment = self.inspection_id.attachment
            else:
                self.x_studio_attachment = None

    @api.constrains('x_studio_part_installed', 'stage_id')
    def _constrains_stage_and_parts(self):
        for record in self:
            if record.stage_id.name == 'Done':
                for part in record.x_studio_part_installed:
                    if part.x_reservation_id.x_studio_status not in ['done', 'rejected'] or part.x_studio_status_1 == 'Not Installed':
                        raise ValidationError(_("There are open transactions or parts not installed."))
