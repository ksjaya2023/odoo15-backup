from odoo import _, api, fields, models
import datetime

_STATUS = [
    ("installed", "Installed"),
    ("not_installed", "Not Installed"),
    ("return", "Return"),
    ("finish", "Finish")
]

_MAINTENANCE_TYPE = [('schedule', 'Schedule'),
                     ('unschedule', 'Unschedule')]


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    _description = 'Maintenance Request or Work Order'

    analytic_code = fields.Char(string='Analytic Code')  # Hide
    close_date = fields.Date(string='Done Date')
    create_reservation = fields.Boolean(string='Create Reservation')
    expence_element = fields.Char(string='Expence Element')
    maintenance_type = fields.Selection(
        string='Maintenance Type', selection_add=_MAINTENANCE_TYPE)
    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic Account')
    maintenance_request_ids = fields.One2many(
        'maintenance.request.line', 'maintenance_request_id', string='')
    reservation_id = fields.Many2one(
        comodel_name='reservation', string='Reservation')
    part_installed_ids = fields.One2many(
        related='reservation_id.reservation_line_ids', readonly=True, string='Part Installed')
    standard_job_id = fields.Many2one('standard.job', string='Standard Job')
    process_id = fields.Many2one('process', string='Process')
    process_activity_id = fields.Many2one(
        'process.line', string='Activity')
    activity_location_id = fields.Many2one(
        'activity.location', string='Location')
    location_department_id = fields.Many2one(
        'activity.location.department', string='Department')
    analytic_group_id = fields.Many2one(
        'department.analytic', string='Analytic Group')
    # account_group = fields.Many2one(
    #     comodel_name='department.analytic', string='Account Group', related='analytic_group_id.account_analytic_group_id')
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment')
    category = fields.Char('Equipment Category',
                           related='equipment_id.eqp_type')

    @api.onchange('standard_job_id')
    def _onchange_standard_job_id(self):
        for record in self:
            if record.standard_job_id:
                record.process_id = record.standard_job_id.process_id.id
                record.process_activity_id = record.standard_job_id.process_line_id.id
                record.activity_location_id = record.standard_job_id.location_id.id
                record.location_department_id = record.standard_job_id.department_id.id
                record.analytic_group_id = record.standard_job_id.analytic_group_id.id
                record.analytic_account_id = record.standard_job_id.analytic_account_id.id

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        for record in self:
            if (record.stage_id.name == 'Done'):
                done_date = datetime.date.today()
                record.close_date = done_date


class MaintenanceRequestLine(models.Model):
    _name = 'maintenance.request.line'
    _description = 'Maintenance Request or Work Order Line'

    name = fields.Char('Description')
    maintenance_request_id = fields.Many2one(
        comodel_name='maintenance.request', string='Maintenance Request ID')
    date = fields.Date('Date')
    sequence = fields.Integer('Sequence', invisible=True)
    status = fields.Selection(selection=_STATUS, string='Status')
    reservation_id = fields.Many2one(
        comodel_name='reservation', string='Reservation')
    product_id = fields.Many2one('product.product', string='Product')
