from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError
from collections import defaultdict
from odoo.tools import float_compare
from odoo.tools.misc import format_date, get_lang, groupby
import json
import re
import logging
_logger = logging.getLogger(__name__)

class EfakturAccountMove(models.Model):
    _inherit = "account.move"

    l10n_id_tax_number_adjustable = fields.Char(string="Nomor Faktur Pajak", copy=False)

    def _post(self, soft=True):
        """Set E-Faktur number after validation."""
        for move in self:
            if move.l10n_id_need_kode_transaksi:
                if not move.l10n_id_kode_transaksi:
                    raise ValidationError(_('You need to put a Kode Transaksi for this partner.'))
                if move.l10n_id_replace_invoice_id.l10n_id_tax_number:
                    if not move.l10n_id_replace_invoice_id.l10n_id_attachment_id:
                        raise ValidationError(_('Replacement invoice only for invoices on which the e-Faktur is generated. '))
                    rep_efaktur_str = move.l10n_id_replace_invoice_id.l10n_id_tax_number
                    tax_number = '%s1%s' % (move.l10n_id_kode_transaksi, rep_efaktur_str[3:])
                    move.l10n_id_tax_number = tax_number
                    move.l10n_id_tax_number_adjustable = tax_number
                else:
                    efaktur = self.env['l10n_id_efaktur.efaktur.range'].pop_number(move.company_id.id)
                    if not efaktur:
                        raise ValidationError(_('There is no Efaktur number available.  Please configure the range you get from the government in the e-Faktur menu. '))
                    tax_number = '%s0%013d' % (str(move.l10n_id_kode_transaksi), efaktur)
                    move.l10n_id_tax_number = tax_number
                    move.l10n_id_tax_number_adjustable = tax_number

        return super(EfakturAccountMove, self)._post(soft)
    
    @api.constrains('l10n_id_tax_number_adjustable')
    def _constrains_l10n_id_tax_number_adjustable(self):
        for record in self.filtered('l10n_id_tax_number_adjustable'):
            if record.l10n_id_tax_number_adjustable != re.sub(r'\D', '', record.l10n_id_tax_number_adjustable):
                record.l10n_id_tax_number_adjustable = re.sub(r'\D', '', record.l10n_id_tax_number_adjustable)
            if len(record.l10n_id_tax_number_adjustable) != 16:
                raise UserError(_('A tax number should have 16 digits'))
            elif record.l10n_id_tax_number_adjustable[:2] not in dict(self._fields['l10n_id_kode_transaksi'].selection).keys():
                raise UserError(_('A tax number must begin by a valid Kode Transaksi'))
            elif record.l10n_id_tax_number_adjustable[2] not in ('0', '1'):
                raise UserError(_('The third digit of a tax number must be 0 or 1'))