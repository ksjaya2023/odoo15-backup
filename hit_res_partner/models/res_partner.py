from odoo import api, fields, models


class ResPartner(models.Model):
  _inherit = 'res.partner'

  is_vendor = fields.Boolean(string='Vendor', default=False)
  is_customer = fields.Boolean(string='Customer', default=False)
