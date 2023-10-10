# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'


    def _get_default_site(self):
        default_site = self.env['md.site'].search([('is_default', '=', True)], limit=1)
        return default_site.id if default_site else None

    purchase_type = fields.Selection([
        ('purchase_request', 'Purchase Request'),
        ('asset_request', 'Asset Request')],
        required=True,
        string='Purchase Type')

    site_id = fields.Many2one('md.site', string='Site', default=_get_default_site)

    # move_state = fields.Selection([
    #     ('draft', 'Pending'),
    #     ('done', 'Done')],
    #     string='Receipt Status',
    #     copy=False,
    #     default='draft',
    #     index=True,
    #     readonly=True,
    #     compute='_compute_move_state',
    #     help="*Following State of the related stock move\n")

    # department = fields.Selection([
    #     ('HCGS', 'HCGS'),
    #     ('PLM', 'PLM'),
    #     ('OPS', 'OPS'),
    #     ('HSE', 'HSE')],
    #     required=True,
    #     string='Department')

    status_asset = fields.Selection([
        ('rental', 'Rental'),
        ('new_purchase', 'New Purchase')],
        store=True,
        string='Status Asset')

    priority = fields.Selection([
        ('P0', 'P0 : 1-3 days'),
        ('P1', 'P1 : 1-7 days'),
        ('P2', 'P2 : 7-15 days'),
        ('P3', 'P3 : >14 days')],
        string='Priority')

    is_direct_payment = fields.Boolean('Direct Payment')


    @api.onchange('picking_type_id')
    def _onchange_picking_type_id(self):
        if self.picking_type_id.warehouse_id:
            self.site_id = self.picking_type_id.warehouse_id.site_id.id
        else:
            self.site_id = False


    # @api.depends('move_count', 'line_ids.move_state', 'write_date', 'line_ids.write_date')
    # def _compute_move_state(self):
    #     for request in self:
    #         all_lines_done = all(line.move_state == 'done' for line in request.line_ids)
    #         new_state = 'done' if all_lines_done else 'draft'

    #         if request.state == 'approved' and new_state == 'done':
    #             request.write({'state': 'done'})
    #         if request.state == 'approved' and new_state == 'draft':
    #             request.write({'state': 'approved'})
    #         if request.state == 'done' and new_state == 'draft':
    #             request.write({'state': 'approved'})
    #         if request.state == 'done' and new_state == 'done':
    #             request.write({'state': 'done'})

    #         request.move_state = new_state




class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order"

    # ---- Inherited Functions ----
    @api.model
    def _prepare_purchase_order(self, picking_type, group_id, company, origin, request, site):
        if not self.supplier_id:
            raise UserError(_("Enter a supplier."))
        supplier = self.supplier_id
        data = {
            "origin": origin,
            "partner_id": self.supplier_id.id,
            "fiscal_position_id": supplier.property_account_position_id
            and supplier.property_account_position_id.id
            or False,
            "picking_type_id": picking_type.id,
            "company_id": company.id,
            "group_id": group_id.id,
            "purchase_request_id": request.id, # Customization on this line
            "site_id": site.id,
        }
        return data


    def make_purchase_order(self):
        res = []
        purchase_obj = self.env["purchase.order"]
        po_line_obj = self.env["purchase.order.line"]
        pr_line_obj = self.env["purchase.request.line"]
        purchase = False

        for item in self.item_ids:
            line = item.line_id
            if item.product_qty <= 0.0:
                raise UserError(_("Enter a positive quantity."))
            if self.purchase_order_id:
                purchase = self.purchase_order_id
            if not purchase:
                po_data = self._prepare_purchase_order(
                    line.request_id.picking_type_id,
                    line.request_id.group_id,
                    line.company_id,
                    line.origin,
                    line.request_id, # Customization on this line
                    line.request_id.site_id,
                )
                purchase = purchase_obj.create(po_data)

            # Look for any other PO line in the selected PO with same
            # product and UoM to sum quantities instead of creating a new
            # po line
            domain = self._get_order_line_search_domain(purchase, item)
            available_po_lines = po_line_obj.search(domain)
            new_pr_line = True
            # If Unit of Measure is not set, update from wizard.
            if not line.product_uom_id:
                line.product_uom_id = item.product_uom_id
            # Allocation UoM has to be the same as PR line UoM
            alloc_uom = line.product_uom_id
            wizard_uom = item.product_uom_id
            if available_po_lines and not item.keep_description:
                new_pr_line = False
                po_line = available_po_lines[0]
                po_line.purchase_request_lines = [(4, line.id)]
                po_line.move_dest_ids |= line.move_dest_ids
                po_line_product_uom_qty = po_line.product_uom._compute_quantity(
                    po_line.product_uom_qty, alloc_uom
                )
                wizard_product_uom_qty = wizard_uom._compute_quantity(
                    item.product_qty, alloc_uom
                )
                all_qty = min(po_line_product_uom_qty, wizard_product_uom_qty)
                self.create_allocation(po_line, line, all_qty, alloc_uom)
            else:
                po_line_data = self._prepare_purchase_order_line(purchase, item)
                if item.keep_description:
                    po_line_data["name"] = item.name
                po_line = po_line_obj.create(po_line_data)
                po_line_product_uom_qty = po_line.product_uom._compute_quantity(
                    po_line.product_uom_qty, alloc_uom
                )
                wizard_product_uom_qty = wizard_uom._compute_quantity(
                    item.product_qty, alloc_uom
                )
                all_qty = min(po_line_product_uom_qty, wizard_product_uom_qty)
                self.create_allocation(po_line, line, all_qty, alloc_uom)
            # TODO: Check propagate_uom compatibility:
            new_qty = pr_line_obj._calc_new_qty(
                line, po_line=po_line, new_pr_line=new_pr_line
            )
            po_line.product_qty = new_qty
            po_line._onchange_quantity()
            # The onchange quantity is altering the scheduled date of the PO
            # lines. We do not want that:
            date_required = item.line_id.date_required
            po_line.date_planned = datetime(
                date_required.year, date_required.month, date_required.day
            )
            res.append(purchase.id)

        return {
            "domain": [("id", "in", res)],
            "name": _("RFQ"),
            "view_mode": "tree,form",
            "res_model": "purchase.order",
            "view_id": False,
            "context": False,
            "type": "ir.actions.act_window",
        }



