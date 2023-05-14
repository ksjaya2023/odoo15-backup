from odoo import api, fields, models


class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"

    # todo: change field name
    @api.onchange("product_id")
    def onchange_product_id(self):
        res = super(PurchaseRequestLine, self).onchange_product_id()
        self.analytic_account_id = self.product_id.product_tmpl_id.cbs_account or False
        return res
