from datetime import datetime
from odoo import _, api, exceptions, fields, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_id = fields.Many2one(
        comodel_name="purchase.request", string="Purchase Request Id", store=False
    )
    purchase_ids = fields.Many2many(
        comodel_name="purchase.request", string="Purchase Request Ids"
    )

    # @api.model
    # def _get_purchase_line_onchange_fields(self):
    #     return ["product_uom", "price_unit", "name", "taxes_id"]

    # @api.model
    # def _execute_purchase_line_onchange(self, vals):
    #     cls = self.env["purchase.order.line"]
    #     onchanges_dict = {
    #         "onchange_product_id": self._get_purchase_line_onchange_fields()
    #     }
    #     for onchange_method, changed_fields in onchanges_dict.items():
    #         if any(f not in vals for f in changed_fields):
    #             obj = cls.new(vals)
    #             getattr(obj, onchange_method)()
    #             for field in changed_fields:
    #                 vals[field] = obj._fields[field].convert_to_write(obj[field], obj)

    # def create_allocation(self, po_line, pr_line, new_qty, alloc_uom):
    #     vals = {
    #         "requested_product_uom_qty": new_qty,
    #         "product_uom_id": alloc_uom.id,
    #         "purchase_request_line_id": pr_line.id,
    #         "purchase_line_id": po_line.id,
    #     }
    #     return self.env["purchase.request.allocation"].create(vals)

    # def _prepare_purchase_order_line(self, po, item):
    #     product = item.product_id
    #     # Keep the standard product UOM for purchase order so we should
    #     # convert the product quantity to this UOM
    #     qty = item.product_uom_id._compute_quantity(
    #         item.product_qty, product.uom_po_id or product.uom_id
    #     )
    #     date_required = item.date_required
    #     vals = {
    #         "name": product.name,
    #         "order_id": self.id,
    #         "product_id": product.id,
    #         "product_uom": product.uom_po_id.id or product.uom_id.id,
    #         "price_unit": po["estimated_cost"],
    #         "product_qty": qty,
    #         "account_analytic_id": item.analytic_account_id.id,
    #         "purchase_request_lines": item,
    #         # "purchase_request_lines": [(6, 0, [item.id])],
    #         # "purchase_request_lines": [(4, item.id)],
    #         "date_planned": datetime(
    #             date_required.year, date_required.month, date_required.day
    #         ),
    #         "move_dest_ids": [(4, x.id) for x in item.move_dest_ids],
    #         "account_analytic_id": product.product_tmpl_id.cbs_account or False,
    #         # "purchase_request_code": item.request_id.id,
    #     }
    #     # self._execute_purchase_line_onchange(vals)
    #     return vals

    # @api.onchange("purchase_id")
    # def _onchange_purchase_id(self):
    #     if self.purchase_id:
    #         # purchase_obj = self.env["purchase.order"]
    #         po_line_obj = self.env["purchase.order.line"]
    #         # pr_line_obj = self.env["purchase.request.line"]
    #         self.purchase_ids = [(4, self.purchase_id.id)]
    #         self.picking_type_id = self.purchase_id.picking_type_id
    #         for line in self.purchase_id.line_ids:
    #             copied_vals = line.copy_data()[0]
    #             po_line_data = self._prepare_purchase_order_line(copied_vals, line)
    #             po_line = po_line_obj.new(po_line_data)

    # # @api.model
    # # def create(self, vals):
    # #     po_line_obj = self.env["purchase.order.line"]
    # #     if vals.get('name', 'New') == 'New':
    # #         seq_date = None
    # #         if 'date_order' in vals:
    # #             seq_date = fields.Datetime.context_timestamp(
    # #                 self, fields.Datetime.to_datetime(vals['date_order']))
    # #         vals['name'] = self.env['ir.sequence'].next_by_code(
    # #             'purchase.order', sequence_date=seq_date) or '/'
    # #     res = super(PurchaseOrder, self).create(vals)
    # #     # for val in vals['order_line']:
    # #     #     po_line_obj.write(val[2])
    # #     # self.create_allocation(po_line, line, all_qty, alloc_uom)
    # #     return res
