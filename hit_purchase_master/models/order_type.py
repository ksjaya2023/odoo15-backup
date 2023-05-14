from odoo import api, fields, models


class OrderType(models.Model):
    _name = "order.type"
    _description = "Order Type"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name", required=True, tracking=True)
