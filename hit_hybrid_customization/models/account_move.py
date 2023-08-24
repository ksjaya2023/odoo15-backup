# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError
from collections import defaultdict
from odoo.tools import float_compare
from odoo.tools.misc import format_date, get_lang


class AccountMove(models.Model):
    _inherit = "account.move"

    site_id = fields.Many2one('md.site', string='Site')

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("to_be_approved", "To Be Approved"),
            ("posted", "Posted"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ]
    )

    def seq_auto_name(self):
        seq = self.env["ir.sequence"].next_by_code("pg.si.inv")
        self.write({"name": seq})

    @api.model
    def create(self, vals):
        create_data = super(AccountMove, self).create(vals)
        if create_data.move_type == "out_invoice":
            if not create_data.name or create_data.name == '/':
                create_data.seq_auto_name()
            return create_data
        else:
            return create_data

    def _get_violated_lock_dates(self, invoice_date, has_tax):
        """Get all the lock dates affecting the current invoice_date.

        :param invoice_date: The invoice date
        :param has_tax: If any taxes are involved in the lines of the invoice
        :return: a list of tuples containing the lock dates affecting this move, ordered chronologically.
        """
        locks = []
        user_lock_date = self.company_id._get_user_fiscal_lock_date()
        if invoice_date and user_lock_date and invoice_date <= user_lock_date:
            locks.append((user_lock_date, _("user")))
        tax_lock_date = self.company_id.tax_lock_date
        if invoice_date and tax_lock_date and has_tax and invoice_date <= tax_lock_date:
            locks.append((tax_lock_date, _("tax")))
        locks.sort()
        return locks

    def _post(self, soft=True):
        """Post/Validate the documents.

        Posting the documents will give it a number, and check that the document is
        complete (some fields might not be required if not posted but are required
        otherwise).
        If the journal is locked with a hash table, it will be impossible to change
        some fields afterwards.

        :param soft (bool): if True, future documents are not immediately posted,
            but are set to be auto posted automatically at the set accounting date.
            Nothing will be performed on those documents before the accounting date.
        :return Model<account.move>: the documents that have been posted
        """
        if soft:
            future_moves = self.filtered(
                lambda move: move.date > fields.Date.context_today(self)
            )
            future_moves.auto_post = True
            for move in future_moves:
                msg = _(
                    "This move will be posted at the accounting date: %(date)s",
                    date=format_date(self.env, move.date),
                )
                move.message_post(body=msg)
            to_post = self - future_moves
        else:
            to_post = self

        # `user_has_group` won't be bypassed by `sudo()` since it doesn't change the user anymore.
        if not self.env.su and not (
            self.env.user.has_group("account.group_account_invoice")
            or self.env.user.has_group(
                "hit_hybrid_customization.group_asset_depreciation"
            )
        ):
            raise AccessError(_("You don't have the access rights to post an invoice."))
        for move in to_post:
            if move.partner_bank_id and not move.partner_bank_id.active:
                raise UserError(
                    _(
                        "The recipient bank account link to this invoice is archived.\nSo you cannot confirm the invoice."
                    )
                )
            if move.state == "posted":
                raise UserError(
                    _("The entry %s (id %s) is already posted.") % (move.name, move.id)
                )
            if not move.line_ids.filtered(lambda line: not line.display_type):
                raise UserError(_("You need to add a line before posting."))
            if move.auto_post and move.date > fields.Date.context_today(self):
                date_msg = move.date.strftime(get_lang(self.env).date_format)
                raise UserError(
                    _("This move is configured to be auto-posted on %s", date_msg)
                )
            if not move.journal_id.active:
                raise UserError(
                    _(
                        "You cannot post an entry in an archived journal (%(journal)s)",
                        journal=move.journal_id.display_name,
                    )
                )

            if not move.partner_id:
                if move.is_sale_document():
                    raise UserError(
                        _(
                            "The field 'Customer' is required, please complete it to validate the Customer Invoice."
                        )
                    )
                elif move.is_purchase_document():
                    raise UserError(
                        _(
                            "The field 'Vendor' is required, please complete it to validate the Vendor Bill."
                        )
                    )

            if (
                move.is_invoice(include_receipts=True)
                and float_compare(
                    move.amount_total, 0.0, precision_rounding=move.currency_id.rounding
                )
                < 0
            ):
                raise UserError(
                    _(
                        "You cannot validate an invoice with a negative total amount. You should create a credit note instead. Use the action menu to transform it into a credit note or refund."
                    )
                )

            if move.display_inactive_currency_warning:
                raise UserError(
                    _(
                        "You cannot validate an invoice with an inactive currency: %s",
                        move.currency_id.name,
                    )
                )

            # Handle case when the invoice_date is not set. In that case, the invoice_date is set at today and then,
            # lines are recomputed accordingly.
            # /!\ 'check_move_validity' must be there since the dynamic lines will be recomputed outside the 'onchange'
            # environment.
            if not move.invoice_date:
                if move.is_sale_document(include_receipts=True):
                    move.invoice_date = fields.Date.context_today(self)
                    move.with_context(
                        check_move_validity=False
                    )._onchange_invoice_date()
                elif move.is_purchase_document(include_receipts=True):
                    raise UserError(
                        _("The Bill/Refund date is required to validate this document.")
                    )

            # When the accounting date is prior to a lock date, change it automatically upon posting.
            # /!\ 'check_move_validity' must be there since the dynamic lines will be recomputed outside the 'onchange'
            # environment.
            affects_tax_report = move._affect_tax_report()
            lock_dates = move._get_violated_lock_dates(move.date, affects_tax_report)
            if lock_dates:
                move.date = move._get_accounting_date(
                    move.invoice_date or move.date, affects_tax_report
                )
                if move.move_type and move.move_type != "entry":
                    move.with_context(check_move_validity=False)._onchange_currency()

        # Create the analytic lines in batch is faster as it leads to less cache invalidation.
        to_post.mapped("line_ids").create_analytic_lines()

        for move in to_post:
            # Fix inconsistencies that may occure if the OCR has been editing the invoice at the same time of a user. We force the
            # partner on the lines to be the same as the one on the move, because that's the only one the user can see/edit.
            wrong_lines = move.is_invoice() and move.line_ids.filtered(
                lambda aml: aml.partner_id != move.commercial_partner_id
                and not aml.display_type
            )
            if wrong_lines:
                wrong_lines.write({"partner_id": move.commercial_partner_id.id})

        to_post.write(
            {
                "state": "posted",
                "posted_before": True,
            }
        )

        for move in to_post:
            move.message_subscribe(
                [
                    p.id
                    for p in [move.partner_id]
                    if p not in move.sudo().message_partner_ids
                ]
            )

            # Compute 'ref' for 'out_invoice'.
            if move._auto_compute_invoice_reference():
                to_write = {
                    "payment_reference": move._get_invoice_computed_reference(),
                    "line_ids": [],
                }
                for line in move.line_ids.filtered(
                    lambda line: line.account_id.user_type_id.type
                    in ("receivable", "payable")
                ):
                    to_write["line_ids"].append(
                        (1, line.id, {"name": to_write["payment_reference"]})
                    )
                move.write(to_write)

        for move in to_post:
            if (
                move.is_sale_document()
                and move.journal_id.sale_activity_type_id
                and (move.journal_id.sale_activity_user_id or move.invoice_user_id).id
                not in (self.env.ref("base.user_root").id, False)
            ):
                move.activity_schedule(
                    date_deadline=min(
                        (
                            date
                            for date in move.line_ids.mapped("date_maturity")
                            if date
                        ),
                        default=move.date,
                    ),
                    activity_type_id=move.journal_id.sale_activity_type_id.id,
                    summary=move.journal_id.sale_activity_note,
                    user_id=move.journal_id.sale_activity_user_id.id
                    or move.invoice_user_id.id,
                )

        customer_count, supplier_count = defaultdict(int), defaultdict(int)
        for move in to_post:
            if move.is_sale_document():
                customer_count[move.partner_id] += 1
            elif move.is_purchase_document():
                supplier_count[move.partner_id] += 1
        for partner, count in customer_count.items():
            (partner | partner.commercial_partner_id)._increase_rank(
                "customer_rank", count
            )
        for partner, count in supplier_count.items():
            (partner | partner.commercial_partner_id)._increase_rank(
                "supplier_rank", count
            )

        # Trigger action for paid invoices in amount is zero
        to_post.filtered(
            lambda m: m.is_invoice(include_receipts=True)
            and m.currency_id.is_zero(m.amount_total)
        ).action_invoice_paid()

        # Force balance check since nothing prevents another module to create an incorrect entry.
        # This is performed at the very end to avoid flushing fields before the whole processing.
        to_post._check_balanced()
        return to_post


    # @api.constrains('invoice_line_ids', 'line_ids')
    # def _check_analytic_account_id(self):
    #     for record in self:
    #         if record.payment_id:
    #             continue
    #         if record.move_type in ('out_invoice', 'in_invoice'):
    #             for journal in record.line_ids:
    #                 if not journal.analytic_account_id:
    #                     continue
    #             for inv_line in record.invoice_line_ids:
    #                 if not inv_line.analytic_account_id:
    #                     raise ValidationError('The analytic account is mandatory.')
    #         if record.move_type in ('entry'):
    #             for journal in record.invoice_line_ids:
    #                 if not journal.analytic_account_id:
    #                     continue
    #             for inv_line in record.line_ids:
    #                 if not inv_line.analytic_account_id:
    #                     raise ValidationError('The analytic account is mandatory.')


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"


    @api.onchange("product_id", "account_id")
    def _onchange_product_id(self):
        if self.product_id or self.account_id:
            self.analytic_account_id = False
            site_id = self.move_id.site_id.id
            if site_id:
                domain = [("site_id", "=", site_id)]
                return {"domain": {"analytic_account_id": domain}}
            else:
                return {"domain": {"analytic_account_id": [("site_id", "=", False)]}}
        else:
            self.analytic_account_id = False
            return {"domain": {"analytic_account_id": [("site_id", "=", False)]}}


