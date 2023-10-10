# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError
from collections import defaultdict
from odoo.tools import float_compare
from odoo.tools.misc import format_date, get_lang
import json
import logging

_logger = logging.getLogger(__name__)


class ReportAccountMove(models.Model):
    _inherit = 'account.move'

    report_tax_totals_json = fields.Char(
        string="Report Tax Totals JSON",
        compute='_compute_report_tax_totals_json',
        )

    @api.depends('tax_totals_json')
    def _compute_report_tax_totals_json(self):
        for record in self:
            report_tax_totals = record.tax_totals_json
            record.report_tax_totals_json = json.dumps(report_tax_totals)
            _logger.info(record.report_tax_totals_json)
    
class CustomTaxReport(models.Model):
    _inherit = "account.move.line"

    tanggal_faktur_pajak = fields.Date('Tanggal Faktur Pajak', related='move_id.tanggal_faktur_pajak')
    tanggal_bukti_potong = fields.Date('Tanggal Bukti Potong', related='move_id.tanggal_bukti_potong')
    amount_tax = fields.Monetary('Amount Tax', related="move_id.amount_tax")
    l10n_id_tax_number = fields.Char('Tax Number', related='move_id.l10n_id_tax_number')
    bill_reference = fields.Char('Bill Reference', related='move_id.bill_reference')
    report_tax_totals_json = fields.Char(string="Report Tax Totals JSON", related="move_id.report_tax_totals_json")


    # Not Used
    @api.model
    def action_view_tax_report(self):
        action = {
            'name': _('Tax Report'),
            'view_mode': 'list',
            'view_id': self.env.ref('hit_hybrid_customization.pg_tax_report_view').id,
            'res_model': 'account.move.line',
            'type': 'ir.actions.act_window',
        }
        return action