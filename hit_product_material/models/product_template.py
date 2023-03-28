from odoo import api, fields, models


class ProductTemplate(models.Model):
  _inherit = 'product.template'

  material_type_id = fields.Many2one(comodel_name='material.type', string='Material Type')
  material_group_id = fields.Many2one(comodel_name='material.group', string='Material Group')
  cbs_account = fields.Many2one('account.analytic.account', string='CBS')