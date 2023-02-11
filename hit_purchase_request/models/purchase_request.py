from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    project_id = fields.Many2one(
        "project.master.data", "Job No.", required=True)
    wbs_id = fields.Many2one("wbs.master.data", "Charge To", required=True)
    purchasing_group_id = fields.Many2one(
        "purchasing.group", "Purchasing Group", required=True
    )
    requester = fields.Char(string="Requester", required=True)

    # @api.model
    # def create(self, vals):
    #     if "line_ids" not in vals.keys():
    #         raise UserError("Data produk tidak ditemukan!")
    #     else:
    #         return super(PurchaseRequest, self).create(vals)

    # def write(self, vals):
    #     if vals.get("line_ids"):
    #         if len(vals["line_ids"]) == 1:
    #             if vals["line_ids"][0][2] == False:
    #                 raise UserError("Data produk tidak ditemukan!")
    #     return super(PurchaseRequest, self).write(vals)
