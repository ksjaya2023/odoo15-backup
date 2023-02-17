from odoo import _, api, fields, models

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

    # account_group = fields.Many2one(
    #     comodel_name='account.analytic.group', string='Account Group')
    analytic_code = fields.Char(string='Analytic Code')  # Hide
    close_date = fields.Date(string='Done Date')
    create_reservation = fields.Boolean(string='Create Reservation')
    expence_element = fields.Char(string='Expence Element')
    maintenance_type = fields.Selection(
        string='Maintenance Type', selection_add=_MAINTENANCE_TYPE)
    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic Account')
    part_installed_id = fields.Many2one(
        'reservation.line', string='Part Installed')
    maintenance_request_ids = fields.One2many(
        'maintenance.request.line', 'maintenance_request_id', string='')
    reservation_id = fields.Many2one(
        comodel_name='reservation', string='Reservation')
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
