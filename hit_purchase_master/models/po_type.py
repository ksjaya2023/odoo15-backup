from odoo import api, fields, models


class PoType(models.Model):
    _name = "po.type"
    _description = "RFQ/PO Type"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name", required=True, tracking=True)
