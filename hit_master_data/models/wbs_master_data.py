from odoo import models, fields, api


class WbsMasterData(models.Model):
  _name = 'wbs.master.data'
  _description = 'WBS Master Data'
  _inherit = ['mail.thread']

  name = fields.Char(string='WBS Code', tracking=True)
  wbs_description = fields.Char(string='WBS Description')
  is_active = fields.Boolean(string='Active', default=True)
  project_id = fields.Many2one('project.master.data', string='Project')
  project_name = fields.Char(string='Project Name', related='project_id.project_name')
  notes = fields.Text(string='Notes')