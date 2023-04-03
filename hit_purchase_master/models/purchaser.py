from odoo import models, fields, api, _


class Purchaser(models.Model):
    _name = "purchaser.master.data"
    _description = "Purchase"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name", required=True, size=3, default="", tracking=True)

    @api.onchange("name")
    def set_caps(self):
        val = str(self.name)
        self.name = val.upper()
