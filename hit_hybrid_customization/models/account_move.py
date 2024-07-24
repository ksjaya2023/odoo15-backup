# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError
from collections import defaultdict
from odoo.tools import float_compare
from odoo.tools.misc import format_date, get_lang, groupby
import json
import re
import logging
_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _apply_inventory(self):
        # For Accounting
        for accounting_date, inventory_ids in groupby(self, key=lambda q: q.accounting_date):
            inventories = self.env['stock.quant'].concat(*inventory_ids)
            if accounting_date:
                user_lock_date = self.company_id._get_user_fiscal_lock_date()
                if accounting_date < user_lock_date:
                    raise ValidationError(f"You cannot adjust the inventory for {accounting_date} because there is a lock period on {user_lock_date}")
                else:
                    super(StockQuant, inventories.with_context(force_period_date=accounting_date))._apply_inventory()
            else:
                super(StockQuant, inventories)._apply_inventory()

class AccountingSequenceMixin(models.AbstractModel):
    _inherit = 'sequence.mixin'

    _pg_custom_regex = r'^SI/(?P<year>\d{4})/PG/(?P<month>\d{2})/(?P<seq>\d{5})$'

    @api.depends(lambda self: [self._sequence_field])
    def _compute_split_sequence(self):
        for record in self:
            sequence = record[record._sequence_field] or ''
            # Custom regex matching for out_invoice
            if record.move_type == 'out_invoice' and record.invoice_date:
                custom_match = re.match(self._pg_custom_regex, sequence)
                if custom_match:
                    record.sequence_prefix = 'SI/{}/PG/{:02d}/'.format(record.invoice_date.year, record.invoice_date.month)
                    record.sequence_number = int(custom_match.group('seq') or 0)
                    continue  # Skip the default handling for custom matches

            regex = re.sub(r"\?P<\w+>", "?:", record._sequence_fixed_regex.replace(r"?P<seq>", ""))  # make the seq the only matching group
            matching = re.match(regex, sequence)
            record.sequence_prefix = sequence[:matching.start(1)]
            record.sequence_number = int(matching.group(1) or 0)
            # _logger.info(f"sequence_prefix: {record.sequence_prefix}")
            # _logger.info(f"sequence_number: {record.sequence_number}")

    @api.model
    def _deduce_sequence_number_reset(self, name):
        """Detect if the used sequence resets yearly, montly or never.

        :param name: the sequence that is used as a reference to detect the resetting
            periodicity. Typically, it is the last before the one you want to give a
            sequence.
        """
        for regex, ret_val, requirements in [
            (self._pg_custom_regex, 'month', ['seq', 'month', 'year']),
            (self._sequence_monthly_regex, 'month', ['seq', 'month', 'year']),
            (self._sequence_yearly_regex, 'year', ['seq', 'year']),
            (self._sequence_fixed_regex, 'never', ['seq']),
        ]:
            match = re.match(regex, name or '')
            # _logger.info(match)
            if match:
                groupdict = match.groupdict()
                if all(req in groupdict for req in requirements):
                    return ret_val
        raise ValidationError(_(
            'The sequence regex should at least contain the seq grouping keys. For instance:\n'
            '^(?P<prefix1>.*?)(?P<seq>\d*)(?P<suffix>\D*?)$'
        ))

    def _set_next_sequence(self):
        """Set the next sequence.

        This method ensures that the field is set both in the ORM and in the database.
        This is necessary because we use a database query to get the previous sequence,
        and we need that query to always be executed on the latest data.

        :param field_name: the field that contains the sequence.
        """
        self.ensure_one()
        last_sequence = self._get_last_sequence()
        new = not last_sequence
        if new:
            last_sequence = self._get_last_sequence(relaxed=True) or self._get_starting_sequence()

        format, format_values = self._get_sequence_format_param(last_sequence)
        if new:
            format_values['seq'] = 0
            format_values['year'] = self[self._sequence_date_field].year % (10 ** format_values['year_length'])
            format_values['month'] = self[self._sequence_date_field].month
        format_values['seq'] = format_values['seq'] + 1
        # _logger.info(f"next format: {format}")
        # _logger.info(f"next format_values: {format_values}")
        self[self._sequence_field] = format.format(**format_values)
        self._compute_split_sequence()

    def _get_sequence_format_param(self, previous):
        """Get the python format and format values for the sequence.

        :param previous: the sequence we want to extract the format from
        :return tuple(format, format_values):
            format is the format string on which we should call .format()
            format_values is the dict of values to format the `format` string
            ``format.format(**format_values)`` should be equal to ``previous``
        """
        sequence_number_reset = self._deduce_sequence_number_reset(previous)
        regex = self._sequence_fixed_regex
        if sequence_number_reset == 'year':
            regex = self._sequence_yearly_regex
        elif sequence_number_reset == 'month':
            regex = self._sequence_monthly_regex

        format_values = re.match(regex, previous).groupdict()
        format_values['seq_length'] = len(format_values['seq'])
        format_values['year_length'] = len(format_values.get('year', ''))
        if not format_values.get('seq') and 'prefix1' in format_values and 'suffix' in format_values:
            # if we don't have a seq, consider we only have a prefix and not a suffix
            format_values['prefix1'] = format_values['suffix']
            format_values['suffix'] = ''
        for field in ('seq', 'year', 'month'):
            format_values[field] = int(format_values.get(field) or 0)

        placeholders = re.findall(r'(prefix\d|seq|suffix\d?|year|month)', regex)
        format = ''.join(
            "{seq:0{seq_length}d}" if s == 'seq' else
            "{month:02d}" if s == 'month' else
            "{year:0{year_length}d}" if s == 'year' else
            "{%s}" % s
            for s in placeholders
        )
        # _logger.info(f"_get_sequence_format_param format: {format}")
        # _logger.info(f"_get_sequence_format_param format_values: {format_values}")
        return format, format_values

    def _get_last_sequence(self, relaxed=False, with_prefix=None, lock=True):
        """Retrieve the previous sequence.

        This is done by taking the number with the greatest alphabetical value within
        the domain of _get_last_sequence_domain. This means that the prefix has a
        huge importance.
        For instance, if you have INV/2019/0001 and INV/2019/0002, when you rename the
        last one to FACT/2019/0001, one might expect the next number to be
        FACT/2019/0002 but it will be INV/2019/0002 (again) because INV > FACT.
        Therefore, changing the prefix might not be convenient during a period, and
        would only work when the numbering makes a new start (domain returns by
        _get_last_sequence_domain is [], i.e: a new year).

        :param field_name: the field that contains the sequence.
        :param relaxed: this should be set to True when a previous request didn't find
            something without. This allows to find a pattern from a previous period, and
            try to adapt it for the new period.
        :param with_prefix: The sequence prefix to restrict the search on, if any.

        :return: the string of the previous sequence or None if there wasn't any.
        """
        self.ensure_one()
        if self._sequence_field not in self._fields or not self._fields[self._sequence_field].store:
            raise ValidationError(_('%s is not a stored field', self._sequence_field))
        where_string, param = self._get_last_sequence_domain(relaxed)
        if self.id or self.id.origin:
            where_string += " AND id != %(id)s "
            param['id'] = self.id or self.id.origin
        if with_prefix is not None:
            where_string += " AND sequence_prefix = %(with_prefix)s "
            param['with_prefix'] = with_prefix

        # query = f"""
        #         SELECT {{field}} FROM {self._table}
        #         {where_string}
        #         AND sequence_prefix = (SELECT sequence_prefix FROM {self._table} {where_string} ORDER BY id DESC LIMIT 1)
        #         ORDER BY sequence_number DESC
        #         LIMIT 1
        # """

        query = f"""
                SELECT {{field}} FROM {self._table}
                {where_string}
                AND (
                    (sequence_prefix IS NULL AND (
                        sequence_prefix = (SELECT sequence_prefix FROM {self._table} {where_string} ORDER BY id DESC LIMIT 1)
                    ) IS NULL) 
                    OR 
                    sequence_prefix = (SELECT sequence_prefix FROM {self._table} {where_string} ORDER BY id DESC LIMIT 1)
                )
                ORDER BY sequence_number DESC
                LIMIT 1
        """

        # _logger.info(f"query: {query}")
        if lock:
            query = f"""
            UPDATE {self._table} SET write_date = write_date WHERE id = (
                {query.format(field='id')}
            )
            RETURNING {self._sequence_field};
            """
        else:
            query = query.format(field=self._sequence_field)

        self.flush([self._sequence_field, 'sequence_number', 'sequence_prefix'])
        self.env.cr.execute(query, param)
        return (self.env.cr.fetchone() or [None])[0]

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
    purchase_request_id = fields.Many2one('purchase.request', string='Purchase Request')
    bill_reference = fields.Char('Bill Reference')
    pg_reversal_id = fields.Many2one('account.move', string="Reverse To", compute='_compute_pg_reversal_id')
    reversed_of_id = fields.Many2one('account.move')
    reversed_by_id = fields.Many2one('account.move', compute='_compute_reversal_id', store=True)
    tanggal_faktur_pajak = fields.Date('Tanggal Faktur Pajak')
    tanggal_bukti_potong = fields.Date('Tanggal Bukti Potong')
    total_discount = fields.Char(compute='_compute_total_discount', string='Total Discount')
    currency_symbol = fields.Char('Currency Symbol', related="currency_id.symbol")

    def _get_last_sequence_domain(self, relaxed=False):
        self.ensure_one()
        if not self.date or not self.journal_id:
            return "WHERE FALSE", {}
        where_string = "WHERE journal_id = %(journal_id)s AND name != '/'"
        param = {'journal_id': self.journal_id.id}

        if not relaxed:
            domain = [('journal_id', '=', self.journal_id.id), ('id', '!=', self.id or self._origin.id), ('name', 'not in', ('/', '', False))]
            if self.journal_id.refund_sequence:
                refund_types = ('out_refund', 'in_refund')
                domain += [('move_type', 'in' if self.move_type in refund_types else 'not in', refund_types)]
            reference_move_name = self.search(domain + [('date', '<=', self.date)], order='date desc', limit=1).name
            if not reference_move_name:
                reference_move_name = self.search(domain, order='date asc', limit=1).name
            sequence_number_reset = self._deduce_sequence_number_reset(reference_move_name)
            if sequence_number_reset == 'year':
                where_string += " AND date_trunc('year', date::timestamp without time zone) = date_trunc('year', %(date)s) "
                param['date'] = self.date
                param['anti_regex'] = re.sub(r"\?P<\w+>", "?:", self._sequence_monthly_regex.split('(?P<seq>')[0]) + '$'
            elif sequence_number_reset == 'month':
                where_string += " AND date_trunc('month', date::timestamp without time zone) = date_trunc('month', %(date)s) "
                param['date'] = self.date
            else:
                param['anti_regex'] = re.sub(r"\?P<\w+>", "?:", self._sequence_yearly_regex.split('(?P<seq>')[0]) + '$'

            if param.get('anti_regex') and not self.journal_id.sequence_override_regex:
                where_string += " AND sequence_prefix !~ %(anti_regex)s "

        if self.journal_id.refund_sequence:
            if self.move_type in ('out_refund', 'in_refund'):
                where_string += " AND move_type IN ('out_refund', 'in_refund') "
            else:
                where_string += " AND move_type NOT IN ('out_refund', 'in_refund') "

        # _logger.info(f"_get_last_sequence_domain where_string: {where_string}")
        # _logger.info(f"_get_last_sequence_domain param: {param}")
        return where_string, param

    def _get_starting_sequence(self):
        self.ensure_one()
        if self.journal_id.type == 'sale':
            starting_sequence = "%s/%04d/00000" % (self.journal_id.code, self.date.year)
        else:
            starting_sequence = "%s/%04d/%02d/0000" % (self.journal_id.code, self.date.year, self.date.month)
        if self.journal_id.refund_sequence and self.move_type in ('out_refund', 'in_refund'):
            starting_sequence = "R" + starting_sequence
        # _logger.info(f"_get_starting_sequence format: {starting_sequence}")
        return starting_sequence

    @api.depends('journal_id', 'date')
    def _compute_highest_name(self):
        for record in self:
            record.highest_name = record._get_last_sequence(lock=False)
            # _logger.info(f"record.highest_name: {record.highest_name}")

    @api.depends('posted_before', 'state', 'journal_id', 'date')
    def _compute_name(self):
        def journal_key(move):
            return (move.journal_id, move.journal_id.refund_sequence and move.move_type)

        def date_key(move):
            return (move.date.year, move.date.month)

        grouped = defaultdict(  # key: journal_id, move_type
            lambda: defaultdict(  # key: first adjacent (date.year, date.month)
                lambda: {
                    'records': self.env['account.move'],
                    'format': False,
                    'format_values': False,
                    'reset': False
                }
            )
        )
        self = self.sorted(lambda m: (m.date, m.ref or '', m.id))
        highest_name = self[0]._get_last_sequence(lock=False) if self else False
        # _logger.info(f"_compute_name highest_name{highest_name}")
        # Group the moves by journal and month
        for move in self:
            if not highest_name and move == self[0] and not move.posted_before and move.date:
                # In the form view, we need to compute a default sequence so that the user can edit
                # it. We only check the first move as an approximation (enough for new in form view)
                pass
            elif (move.name and move.name != '/') or move.state != 'posted':
                try:
                    if not move.posted_before:
                        move._constrains_date_sequence()
                    # Has already a name or is not posted, we don't add to a batch
                    continue
                except ValidationError:
                    # Has never been posted and the name doesn't match the date: recompute it
                    pass
            group = grouped[journal_key(move)][date_key(move)]
            if not group['records']:
                # Compute all the values needed to sequence this whole group
                move._set_next_sequence()
                group['format'], group['format_values'] = move._get_sequence_format_param(move.name)
                group['reset'] = move._deduce_sequence_number_reset(move.name)
            group['records'] += move

        # Fusion the groups depending on the sequence reset and the format used because `seq` is
        # the same counter for multiple groups that might be spread in multiple months.
        final_batches = []
        for journal_group in grouped.values():
            journal_group_changed = True
            for date_group in journal_group.values():
                if (
                    journal_group_changed
                    or final_batches[-1]['format'] != date_group['format']
                    or dict(final_batches[-1]['format_values'], seq=0) != dict(date_group['format_values'], seq=0)
                ):
                    final_batches += [date_group]
                    journal_group_changed = False
                elif date_group['reset'] == 'never':
                    final_batches[-1]['records'] += date_group['records']
                elif (
                    date_group['reset'] == 'year'
                    and final_batches[-1]['records'][0].date.year == date_group['records'][0].date.year
                ):
                    final_batches[-1]['records'] += date_group['records']
                else:
                    final_batches += [date_group]

        # Give the name based on previously computed values
        for batch in final_batches:
            for move in batch['records']:
                move.name = batch['format'].format(**batch['format_values'])
                batch['format_values']['seq'] += 1
            batch['records']._compute_split_sequence()
            # _logger.info(f"final_batches: {final_batches}")
            # _logger.info(f"name: {move.name}")

        self.filtered(lambda m: not m.name).name = '/'


    # ---- Computed Fields ----


    @api.depends('invoice_line_ids')
    def _compute_total_discount(self):
        for record in self:
            total_discount_val = 0
            total_discount_val = sum(record.invoice_line_ids.mapped("discount_val"))
            record.total_discount = total_discount_val

    @api.depends('reversed_entry_id')
    def _compute_pg_reversal_id(self):
        for record in self:
            dest_reversal = record.env['account.move'].search([("reversed_entry_id", "=", record.id)], limit=1)
            if dest_reversal:
                record.pg_reversal_id = dest_reversal.id
            else:
                record.pg_reversal_id = False

    @api.depends('reversed_of_id')
    def _compute_reversal_id(self):
        for record in self:
            dest_reversal = record.env['account.move'].search([("reversed_of_id", "=", record.id)], limit=1)
            if dest_reversal:
                record.reversed_by_id = dest_reversal.id
            else:
                record.reversed_by_id = False

    @api.onchange('invoice_line_ids')
    def pg_onchange_invoice_line_ids(self):
        for rec in self:
            for line in rec.invoice_line_ids:
                line.pg_compute_discount()
                line.pg_compute_discount_val()

    @api.onchange('invoice_date')
    def _onchange_invoice_date_pg_custom(self):
        if self.move_type == 'out_invoice' and self.invoice_date:
            self.tanggal_faktur_pajak = self.invoice_date


    def button_cancel(self):
        res = super().button_cancel()
        for record in self:
            record.write({"reversed_of_id": False})
        return res

    def action_reverse(self):
        res = super().action_reverse()
        for record in self:
            if record.move_type == 'in_invoice':
                refund_records = record.env['account.move'].search([('reversed_of_id', '=', record.id), ('move_type', '=', 'in_refund')])
                for refund_record in refund_records:
                    if refund_record and record.reversed_of_id.id:
                        raise ValidationError(_("Dokumen sudah dilakukan reverse dengan dokumen %s") % refund_records.name)
                record.write({"reversed_of_id": record.id})
            elif record.move_type == 'out_invoice':
                refund_records = record.env['account.move'].search([('reversed_of_id', '=', record.id), ('move_type', '=', 'out_refund')])
                for refund_record in refund_records:
                    if refund_record and record.reversed_of_id.id:
                        raise ValidationError(_("Dokumen sudah dilakukan reverse dengan dokumen %s") % refund_records.name)
                record.write({"reversed_of_id": record.id})
        return res

    def button_cancel(self):
        res = super().button_cancel()
        for record in self:
            record.write({"reversed_of_id": False})
        return res

    def action_reverse(self):
        res = super().action_reverse()
        for record in self:
            if record.move_type == 'in_invoice':
                refund_records = record.env['account.move'].search([('reversed_of_id', '=', record.id), ('move_type', '=', 'in_refund')])
                for refund_record in refund_records:
                    if refund_record and record.reversed_of_id.id:
                        raise ValidationError(_("Dokumen sudah dilakukan reverse dengan dokumen %s") % refund_records.name)
                record.write({"reversed_of_id": record.id})
            elif record.move_type == 'out_invoice':
                refund_records = record.env['account.move'].search([('reversed_of_id', '=', record.id), ('move_type', '=', 'out_refund')])
                for refund_record in refund_records:
                    if refund_record and record.reversed_of_id.id:
                        raise ValidationError(_("Dokumen sudah dilakukan reverse dengan dokumen %s") % refund_records.name)
                record.write({"reversed_of_id": record.id})
        return res

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



class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    discount_val = fields.Float(string="Discount Value")


    def pg_compute_discount_val(self):
        for record in self:
            if record.discount:
                record.discount_val = 0
                discount_val = (record.discount / 100) * (record.quantity * record.price_unit)
                record.discount_val = discount_val


    def pg_compute_discount(self):
        for record in self:
            if record.discount_val:
                record.discount = 0
                discount = (record.discount_val / (record.quantity * record.price_unit)) * 100
                record.discount = discount


    # ---- Onchanges ----


    @api.onchange('discount','price_unit', 'quantity')
    def _onchange_discount(self):
        self.pg_compute_discount_val()


    @api.onchange('discount_val','price_unit', 'quantity')
    def _onchange_discount_val(self):
        self.pg_compute_discount()


    @api.onchange("product_id", "account_id")
    def _onchange_product_id(self):
        if self.product_id or self.account_id:
            self.analytic_account_id = False
            site_id = self.move_id.site_id.id
            if site_id:
                domain = [("site_id", "=", site_id)]
                return {"domain": {"analytic_account_id": domain}}
            else:
                return {"domain": {"analytic_account_id": [("site_id", "=", True)]}}
        else:
            self.analytic_account_id = False
            return {"domain": {"analytic_account_id": [("site_id", "=", True)]}}






