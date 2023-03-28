from odoo import api, fields, models


class PrType(models.Model):
    _name = "pr.type"
    _description = "PR Type"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name", required=True, tracking=True)
