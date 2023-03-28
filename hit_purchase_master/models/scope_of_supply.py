from odoo import models, fields, api, _


class ScopeOfSupply(models.Model):
    _name = "scope.of.supply"
    _description = "Scope of Supply"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name", required=True, default="", tracking=True)
    active = fields.Boolean(string="Active", default=True)
    fullname = fields.Char(string="Full Name")

    @api.onchange("name")
    def set_caps(self):
        val = str(self.name)
        self.name = val.upper()
