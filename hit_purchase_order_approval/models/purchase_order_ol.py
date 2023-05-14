from odoo import api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    approval_sec = fields.Integer(string='Approval Stages', default='0')
    purchasing_group_rel = fields.Char(
        related='x_studio_purchasing_group.x_name')
    approval_a = fields.Many2one(
        comodel_name='res.users', string='Approval 1')
    approval_b = fields.Many2one(
        comodel_name='res.users', string='Approval 2')
    approval_c = fields.Many2one(
        comodel_name='res.users', string='Approval 3')
    approval_d = fields.Many2one(
        comodel_name='res.users', string='Approval 4')

    def _check_user_id(self, cur, tar):
        return cur == tar

    def action_release(self):
        if (self.state == 'to approve' or self.state == 'purchase' and self.approval_sec < 4):
            data_dict = {
                0: self.approval_a.id,
                1: self.approval_b.id,
                2: self.approval_c.id,
                3: self.approval_d.id,
            }
            current_user_id = self._uid
            seq = self.approval_sec
            target_id = data_dict[seq]
            checked = self._check_user_id(current_user_id, target_id)
            if (self.purchasing_group_rel != 'Buyer HO'):
                if checked and seq == 2:
                    self.state = 'done'
                    seq += 1
                    self.approval_sec = seq
                elif checked and seq < 2:
                    seq += 1
                    self.approval_sec = seq
                else:
                    raise UserError('Anda tidak memiliki hak untuk release!')
            else:
                if checked and seq == 3:
                    self.state = 'done'
                    seq += 1
                    self.approval_sec = seq
                elif checked and seq < 3:
                    seq += 1
                    self.approval_sec = seq
                else:
                    raise UserError('Anda tidak memiliki hak untuk release!')
        else:
            raise UserError('Anda tidak dapat melakukan release lagi!')

    def action_unrelease(self):
        if (self.state == 'to approve' or self.state == 'purchase') and self.approval_sec > 0:
            data_dict = {
                0: self.approval_a.id,
                1: self.approval_b.id,
                2: self.approval_c.id,
                3: self.approval_d.id,
            }
            current_user_id = self._uid
            seq = self.approval_sec - 1
            target_id = data_dict[seq]
            checked = self._check_user_id(current_user_id, target_id)
            if (checked):
                self.approval_sec = seq
            else:
                raise UserError('Anda tidak memiliki hak untuk unrelease!')
        else:
            raise UserError('Data belum ada melakukan release!')
