from odoo import api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class ProjectMasterData(models.Model):
  _name = 'project.master.data'
  _description = 'Project Master Data'
  _inherit = ['mail.thread']

  name = fields.Char(string='Project Code', tracking=True)
  project_name = fields.Char(string='Project Name')
  address = fields.Char(string='Address')
  project_description = fields.Text(string='Project Description')
  customer = fields.Many2one('res.partner', string='Customer')
  project_start = fields.Date(string='Project Start')
  project_end = fields.Date(string='Project End')
  is_active = fields.Boolean(string='Active?')
