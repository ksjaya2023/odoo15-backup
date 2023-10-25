# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
import json
import logging

_logger = logging.getLogger(__name__)


class ReportAccountMove(models.Model):
    _inherit = 'account.move'

    report_tax_totals_json = fields.Char(
        string="Report Tax Totals JSON",
        compute='_compute_report_tax_totals_json',
        )
    ppn_value = fields.Float(string="PPN", compute='_compute_report_tax_totals_json', store=True)
    pph_value = fields.Float(string="PPh", compute='_compute_report_tax_totals_json', store=True)
    tax_group_names = fields.Char(string="Taxes", compute='_compute_report_tax_totals_json', store=True)
    has_tax_line_id = fields.Boolean(compute='_compute_has_tax_line_id', string='Has Tax Line Id', store=True)
    tax_base_amount = fields.Monetary(string="Base Amount", store=True, readonly=True, currency_field='company_currency_id', compute='_compute_has_tax_line_id')
    
    @api.depends('tax_totals_json')
    def _compute_has_tax_line_id(self):
        for record in self:
            has_tax_line = record.env['account.move.line'].search([
                ('move_id', '=', record.id),
                ('tax_line_id', '!=', False)
            ], limit=1)
            record.has_tax_line_id = bool(has_tax_line)
            record.tax_base_amount = has_tax_line.tax_base_amount if has_tax_line else 0


    @api.depends('tax_totals_json')
    def _compute_report_tax_totals_json(self):
        for record in self:
            if record.tax_totals_json:
                parsed_data = json.loads(record.tax_totals_json)
                ppn_value = 0.0
                pph_value = 0.0
                tax_group_names = set()

                if 'groups_by_subtotal' in parsed_data:
                    for group in parsed_data['groups_by_subtotal'].values():
                        for item in group:
                            tax_group_name = item.get('tax_group_name', '')
                            tax_group_amount = item.get('tax_group_amount', 0.0)

                            tax_group_names.add(tax_group_name)
                            
                            if 'ppn' in tax_group_name.lower():
                                ppn_value = tax_group_amount
                            elif 'pph' in tax_group_name.lower():
                                pph_value = tax_group_amount

                record.report_tax_totals_json = json.dumps(parsed_data)
                record.ppn_value = ppn_value
                record.pph_value = pph_value
                record.tax_group_names = ', '.join(tax_group_names)
            else:
                record.report_tax_totals_json = False
                record.ppn_value = 0.0
                record.pph_value = 0.0
                record.tax_group_names = False
    
class CustomTaxReport(models.Model):
    _inherit = "account.move.line"

    tanggal_faktur_pajak = fields.Date('Tanggal Faktur Pajak', related='move_id.tanggal_faktur_pajak')
    tanggal_bukti_potong = fields.Date('Tanggal Bukti Potong', related='move_id.tanggal_bukti_potong')
    amount_tax = fields.Monetary('Amount Tax', related="move_id.amount_tax")
    l10n_id_tax_number = fields.Char('Tax Number', related='move_id.l10n_id_tax_number')
    bill_reference = fields.Char('Bill Reference', related='move_id.bill_reference')
    report_tax_totals_json = fields.Char(string="Report Tax Totals JSON", related="move_id.report_tax_totals_json")
    ppn_value = fields.Float(string="PPN", related="move_id.ppn_value")
    pph_value = fields.Float(string="PPh", related="move_id.pph_value")
    tax_group_names = fields.Char(string="Taxes", related='move_id.tax_group_names')


    # Not Used
    # @api.model
    # def action_view_tax_report(self):
    #     action = {
    #         'name': _('Tax Report'),
    #         'view_mode': 'list',
    #         'view_id': self.env.ref('hit_hybrid_customization.pg_tax_report_view').id,
    #         'res_model': 'account.move.line',
    #         'type': 'ir.actions.act_window',
    #     }
    #     return action