from odoo import _, api, fields, models


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    account_group = fields.Many2one(
        comodel_name='account.analytic.group', string='Account Group')
    analytic_code = fields.Char(string='Analytic Code')
    category = fields.Char(string='Category')
    close_date = fields.Date(string='Done Date')
    create_reservation = fields.Boolean(string='Create Reservation')
    expence_element = fields.Char(string='Expence Element')
    # I don't know why the technical name is 'schedulle', I want to change it but it might break the whole system
    maintenance_type = fields.Selection(string='Maintenance Type', selection=[
                                        ('Schedulle', 'Schedule'), ('Unschedulle', 'Unschedule')])
    analytic_account = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic Account')
