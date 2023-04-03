from odoo import models, fields, api, _


class ProjectMasterData(models.Model):
    _inherit = 'project.master.data'

    purchasing_group_id = fields.Many2many("purchasing.group", string="Purchasing Group")

