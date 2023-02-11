from odoo import _, api, fields, models


class StandardJob(models.Model):
    _name = 'standard.job'
    _description = 'Standard Job for Master Data Equipment'

    name = fields.Char(string='Standard Job')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')
    # account_group = fields.Many2one(
    #     comodel_name='account.analytic.group', string='Account Group')  # related
    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic Account')
    notes = fields.Html(string='Notes')
