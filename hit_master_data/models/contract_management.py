from odoo import api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class ContractManagement(models.Model):
  _name = 'contract.master.data'
  _description = 'Description'
  _inherit = ['mail.thread']

  name = fields.Char(string='Contract Number', tracking=True)
  project_id = fields.Many2one('project.master.data', string='Project/Job No.')
  customer_id = fields.Many2one('res.partner', string='Customer')
  address = fields.Char(string='Address', readonly=True, related='customer_id.street')
  payment_bank = fields.Char(string='Bank Name')
  account_no = fields.Char(string='Bank Account')
  bank_branch = fields.Char(string='Branch')
  scope_of_contract = fields.Text(string='Contract Details')
  contract_duration = fields.Integer(string='Duration')
  contract_time = fields.Selection([('Year', 'Year'), ('Month', 'Month'), 
    ('Week', 'Week'), ('Day', 'Day')], string='Time')
  start_of_contract = fields.Date(string='Start of Contract')
  end_of_contract = fields.Date(string='End of Contract')
  contract_addendum = fields.Float(string='Addendum')
  currency_id = fields.Many2one('res.currency', string="Currency")
  contract_amount = fields.Monetary(string='Contract Amount')
  other_information = fields.Text(string='Other Information')
  scan_of_contract = fields.Binary(string='Scan of Contract', attachment=True)
  state = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('done', 'Done')], default='draft')
  currency_id = fields.Many2one('res.currency', string="Currency", required=True, 
    default=lambda self: self.env.company.currency_id.id)
  account_move_ids = fields.One2many('account.move', 'contract_id', string='Account Move', store=True)
  x_css = fields.Html(
        string='CSS',
        sanitize=False,
        compute='_compute_css',
        store=False,
    )

  # hide Edit button based on state
  @api.depends('state')
  def _compute_css(self):
    for application in self:
      if application.state == 'done':
        application.x_css = '<style>.o_form_button_edit {display: none !important;}</style>'
      else:
        application.x_css = False

  def activate_contract(self):
    self.write({'state': 'active'})

  def complete_contract(self):
    self.write({'state': 'done'})

  def set_to_draft(self):
    self.write({'state': 'draft'})