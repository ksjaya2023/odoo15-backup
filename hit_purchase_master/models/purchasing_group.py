from odoo import models, fields, api, _


class PurchasingGroup(models.Model):
    _name = "purchasing.group"
    _description = "Purchase Group"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name", required=True, tracking=True)
    purchaser_id = fields.Many2one(
        comodel_name="purchaser.master.data", string="Purchaser"
    )
    picking_type_id = fields.Many2many("stock.picking.type", string="Picking Type")
