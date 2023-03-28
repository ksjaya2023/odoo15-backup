from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    contract_id = fields.Many2one('contract.master.data', string='Contract')

    @api.onchange("contract_id")
    def _onchange_contract_id(self):
        val = self.contract_id.customer_id.id
        self.partner_id = val
 
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    m_wbs_code = fields.Many2one('wbs.master.data', string='WBS Code')
