from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    discount_type = fields.Selection(
        [
            ("percent", "By Percentage"),
            ("price", "By Price"),
        ],
        "Discount Type",
        default="percent",
    )
    revision_counts = fields.Integer("Revisions", readonly=True, store=True, default=0)
    freight_category = fields.Selection(
        [("include", "Include"), ("exclude", "Exclude")],
        "Freight Category",
        default="include",
    )

    def print_quotation(self):
        self.write({"state": "sent"})
        return self.env.ref(
            "hit_purchase_enhancement.report_purchase_quotation"
        ).report_action(self)

    @api.onchange("discount_type")
    def onchange_discount_type(self):
        for record in self.order_line:
            if record.discount_type == "percent":
                record.discount_rp = None
            if record.discount_type == "price":
                record.discount = None

    def write(self, vals):
        if vals.get("order_line") and self.state == "purchase":
            edited = False
            for record in vals["order_line"]:
                if record[2] != False:
                    edited = True
            if edited:
                vals["revision_counts"] = self.revision_counts + 1
        return super(PurchaseOrder, self).write(vals)


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    # adding discount to depends
    @api.depends("discount", "discount_rp", "freight_cost", "order_id.freight_category")
    def _compute_amount(self):
        super(PurchaseOrderLine, self)._compute_amount()
        for line in self:
            vals = line._prepare_compute_all_values()
            price_unit_temp = vals["price_unit"] - (
                vals["freight_cost"]
                if line.order_id.freight_category == "exclude"
                else 0
            )
            taxes = line.taxes_id.compute_all(
                price_unit_temp,
                vals["currency_id"],
                vals["product_qty"],
                vals["product"],
                vals["partner"],
            )
            line.update(
                {
                    "price_tax": sum(
                        t.get("amount", 0.0) for t in taxes.get("taxes", [])
                    ),
                    "price_total": taxes["total_included"],
                    "price_subtotal": taxes["total_excluded"]
                    + (
                        vals["freight_cost"]
                        if line.order_id.freight_category == "exclude"
                        else 0
                    ),
                }
            )

    def _prepare_compute_all_values(self):
        vals = super()._prepare_compute_all_values()
        vals.update(
            {"price_unit": self._get_discounted_price_unit() + self.freight_cost}
        )
        vals.update({"freight_cost": self.freight_cost})
        return vals

    def _get_discounted_price_unit(self):
        """Inheritable method for getting the unit price after applying
        discount(s).

        :rtype: float
        :return: Unit price after discount(s).
        """
        self.ensure_one()
        if self.discount:
            return self.price_unit * (1 - self.discount / 100)
        if self.discount_rp:
            return self.price_unit - (self.discount_rp / self.product_qty)
        return self.price_unit

    discount_type = fields.Selection(related="order_id.discount_type")
    discount = fields.Float(string="Discount (%)", digits="Discount")
    discount_rp = fields.Float(string="Discount by Price", digits="Discount by Price")
    freight_cost = fields.Float("Freight Cost")

    _sql_constraints = [
        (
            "discount_limit",
            "CHECK (discount <= 100.0)",
            "Discount must be lower than 100%.",
        )
    ]

    def _get_stock_move_price_unit(self):
        res = super(PurchaseOrderLine, self)._get_stock_move_price_unit()
        if self.discount:
            res = res * (1 - self.discount / 100)
        if self.discount_rp:
            res = res - (self.discount_rp / self.product_qty)
        res += self.freight_cost
        return res

    def _prepare_account_move_line(self, move=False):
        vals = super(PurchaseOrderLine, self)._prepare_account_move_line(move)
        vals.update(
            {"price_unit": self._get_discounted_price_unit() + self.freight_cost}
        )
        return vals
