# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError, ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    project_id = fields.Many2one(comodel_name="project.master.data", string="Job No.")
    sub_job = fields.Char(string="Sub Job")
    transfer_user = fields.Char(string="User")
    transfer_level = fields.Char(string="Level")
    transfer_issued_by = fields.Char(string="Issue/Receipt/Sender by")
    reference_doc = fields.Char(string="Reference Document")
    transported_by = fields.Char(string="Transported By")
    loading_unloading = fields.Char(string="Loading/Unloading")
    vehicle_no = fields.Char(string="Vehicle No.")


class StockMove(models.Model):
    _inherit = "stock.move"

    po_way_bill = fields.Char(string="PO Way Bill")
    wbs_id = fields.Many2one("wbs.master.data", string="WBS Code")
    rel_job_no = fields.Char(string='Related Job Number', related="picking_id.project_id.name")

    @api.onchange('rel_job_no')
    def onchange_job_no(self):
        code = self.rel_job_no
        return {
            'domain': {
                'wbs_id':
                [('project_id.name', '=', code)]
            }
        }


    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, 
        credit_value, debit_account_id, credit_account_id, description):
        # This method returns a dictionary to provide an easy extension hook
        # to modify the valuation lines (see purchase for an example)
        self.ensure_one()

        debit_account_code = self.env['account.account'].search(
            [('id', '=', debit_account_id)]).code[:1]
        credit_account_code = self.env['account.account'].search(
            [('id', '=', credit_account_id)]).code[:1]

        debit_wbs_code_id = self.wbs_id.id
        credit_wbs_code_id = self.wbs_id.id

        # check if kepala account = 1 then jangan assign nilai wbs
        if credit_account_code == '1':
            credit_wbs_code_id = False
        if debit_account_code == '1':
            debit_wbs_code_id = False

        debit_line_vals = {
            'name': description,
            'product_id': self.product_id.id,
            'quantity': qty,
            'product_uom_id': self.product_id.uom_id.id,
            'ref': description,
            'partner_id': partner_id,
            'debit': debit_value if debit_value > 0 else 0,
            'credit': -debit_value if debit_value < 0 else 0,
            'account_id': debit_account_id,
            'wbs_code': debit_wbs_code_id,
        }

        credit_line_vals = {
            'name': description,
            'product_id': self.product_id.id,
            'quantity': qty,
            'product_uom_id': self.product_id.uom_id.id,
            'ref': description,
            'partner_id': partner_id,
            'credit': credit_value if credit_value > 0 else 0,
            'debit': -credit_value if credit_value < 0 else 0,
            'account_id': credit_account_id,
            'wbs_code': credit_wbs_code_id,
        }

        rslt = {'credit_line_vals': credit_line_vals,
                'debit_line_vals': debit_line_vals}
        if credit_value != debit_value:
            # for supplier returns of product in average costing method, in anglo saxon mode
            diff_amount = debit_value - credit_value
            price_diff_account = self.product_id.property_account_creditor_price_difference

            if not price_diff_account:
                price_diff_account = self.product_id.categ_id.property_account_creditor_price_difference_categ
            if not price_diff_account:
                raise UserError(
                    _('Configuration error. Please configure the price difference account on the product or its category to process this operation.'))

            rslt['price_diff_line_vals'] = {
                'name': self.name,
                'product_id': self.product_id.id,
                'quantity': qty,
                'product_uom_id': self.product_id.uom_id.id,
                'ref': description,
                'partner_id': partner_id,
                'credit': diff_amount > 0 and diff_amount or 0,
                'debit': diff_amount < 0 and -diff_amount or 0,
                'account_id': price_diff_account.id,
            }
        return rslt

    # def _create_account_move_line(self, credit_account_id, debit_account_id, 
    #     journal_id, qty, description, svl_id, cost):
    #     self.ensure_one()
    #     AccountMove = self.env['account.move'].with_context(
    #         default_journal_id=journal_id)

    #     move_lines = self._prepare_account_move_line(
    #         qty, cost, credit_account_id, debit_account_id, description)
    #     if move_lines:
    #         date = self._context.get(
    #             'force_period_date', fields.Date.context_today(self))
    #         new_account_move = AccountMove.sudo().create({
    #             'journal_id': journal_id,
    #             'line_ids': move_lines,
    #             'date': date,
    #             'ref': description,
    #             'stock_move_id': self.id,
    #             'stock_valuation_layer_ids': [(6, None, [svl_id])],
    #             'move_type': 'entry',
    #             'x_studio_projectjob_no': self.picking_id.x_studio_job_no.id,
    #             'x_studio_document_date': datetime.today(),
    #         })

    #         # code generator
    #         journal_id = new_account_move.journal_id.code
    #         journal_indicator = new_account_move.journal_id.x_studio_journal_indicator
    #         project_name = ''
    #         key = ''
    #         name = ''

    #         if new_account_move.x_studio_projectjob_no.x_name is not False:
    #             name = new_account_move.x_studio_projectjob_no.x_name
    #             if name == 'Head Office':
    #                 name = 'HO'
    #             project_name = 'TPE/' + journal_id + '/' + name + '/'

    #         if journal_indicator == 'bank' and \
    #                 new_account_move.x_studio_payment_type is not False:
    #             project_name = 'TPE/' + journal_id + '/' + \
    #                 new_account_move.x_studio_payment_type.upper() + '/' + name + '/'
    #         key = project_name

    #         num = 1
    #         date = new_account_move.date.strftime('%Y/%m')
    #         draft_sequence = key + date
    #         last_record = self.env['account.move'].search_count(
    #             [('name', '=ilike', draft_sequence + '%')])
    #         if last_record > 0:
    #             temp = self.env['account.move'].search(
    #                 [('name', '=ilike', draft_sequence + '%')], order='name desc', limit=1).name
    #             temp_seq = temp[-4:]
    #             num = int(temp_seq) + 1
    #         seq = '{0:04}'.format(num)
    #         new_account_move.name = draft_sequence + '/' + seq

    #         new_account_move._post()