from odoo import _, api, fields, models

_STATUS = [
    ("installed", "Installed"),
    ("not_installed", "Not Installed"),
    ("return", "Return"),
    ("finish", "Finish")
]


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    _description = 'Maintenance Request or Work Order'

    # account_group = fields.Many2one(
    #     comodel_name='account.analytic.group', string='Account Group')
    analytic_code = fields.Char(string='Analytic Code')
    category = fields.Char(string='Categories')
    close_date = fields.Date(string='Done Date')
    create_reservation = fields.Boolean(string='Create Reservation')
    expence_element = fields.Char(string='Expence Element')
    # I don't know why the technical name is 'schedulle', I want to change it but it might break the whole system
    # maintenance_type = fields.Selection(string='Maintenance Type', selection=[
    #                                     ('Schedule', 'Schedule'), ('Unschedule', 'Unschedule')])
    analytic_account = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic Account')
    maintenance_request_ids = fields.One2many(
        'maintenance.request.line', 'maintenance_request_id', string='Maintenance Request Ids')


class MaintenanceRequestLine(models.Model):
    _name = 'maintenance.request.line'
    _description = 'Maintenance Request or Work Order Line'

    name = fields.Char('Description')
    maintenance_request_id = fields.Many2one(
        comodel_name='maintenance.request', string='Maintenance Request ID')
    date = fields.Date('Date')
    sequence = fields.Integer('Sequence')
    status = fields.Selection(selection=_STATUS, string='Status')
