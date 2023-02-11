from odoo import api, fields, models, _


class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"
    _order = "id asc"

    # # todo: change field name
    # @api.onchange("product_id")
    # def onchange_product_id(self):
    #     res = super(PurchaseRequestLine, self).onchange_product_id()
    #     self.analytic_account_id = self.product_id.product_tmpl_id.cbs_account or False
    #     return res

    # def copy_data(self, default=None):
    #     if default is None:
    #         default = {}
    #     return super(PurchaseRequestLine, self).copy_data(default)
