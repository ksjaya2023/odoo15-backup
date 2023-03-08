from odoo import _, api, fields, models


class StandardJob(models.Model):
    _name = 'standard.job'
    _description = 'Standard Job for Master Data Equipment'

    name = fields.Char(string='Standard Job')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')
    process_id = fields.Many2one('hit.process', string='Process')
    process_line_id = fields.Many2one('hit.process.line', string='Activity')
    location_id = fields.Many2one('hit.activity.location', string='Location')
    department_id = fields.Many2one(
        'hit.activity.location.department', string='Department')
    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic Account')
    analytic_group_id = fields.Many2one(
        'hit.department.analytic', string='Analytic Group')
    # account_group = fields.Many2one(
    #     comodel_name='account.analytic.group', string='Account Group')  # related
    notes = fields.Html(string='Notes')
