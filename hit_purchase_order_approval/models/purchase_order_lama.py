from odoo import api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from datetime import date, datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from lxml import etree


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    approval_sec = fields.Integer(
        string='Approval Stages', default='0', tracking=True)
    purchasing_group_rel = fields.Char(
        related='x_studio_many2one_field_8l3kA.x_name')
    # purchasing_group_rel = fields.Char(
    #     related='x_studio_purchasing_group.x_name')
    user_eligibility_release = fields.Boolean(
        string='User eligibility release', default=False, compute='_check_whos_responsible')
    user_eligibility_unrelease = fields.Boolean(
        string='User eligibility unrelease', default=False, compute='_check_whos_responsible')
    current_user = fields.Many2one(
        'res.users', default=lambda self: self.env.uid)
    next_approval = fields.Many2one(
        comodel_name='res.users', string='Next Approval', readonly="1",
        compute='_check_whos_responsible', tracking=True, store=True)
    approval_a = fields.Many2one(
        comodel_name='res.users', string='Approval 1')
    approval_b = fields.Many2one(
        comodel_name='res.users', string='Approval 2')
    approval_c = fields.Many2one(
        comodel_name='res.users', string='Approval 3')
    approval_d = fields.Many2one(
        comodel_name='res.users', string='Approval 4')
    approval_a_time = fields.Datetime(string='Approval 1 Time')
    approval_b_time = fields.Datetime(string='Approval 2 Time')
    approval_c_time = fields.Datetime(string='Approval 3 Time')
    approval_d_time = fields.Datetime(string='Approval 4 Time')
    x_css = fields.Html(
        string='CSS',
        sanitize=False,
        compute='_compute_css',
        store=False,
    )

    # hide Edit button based on state
    @api.depends('state')
    def _compute_css(self):
        for application in self:
            if application.state != 'draft':
                application.x_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                application.x_css = False

    # TODO: Rewrite code and testing
    @api.depends('approval_sec', 'approval_a', 'approval_b', 'approval_c', 'approval_d', 'user_eligibility_release', 'user_eligibility_unrelease')
    def _check_whos_responsible(self):
        for record in self:
            data_dict = {
                0: record.approval_a.id,
                1: record.approval_b.id,
                2: record.approval_c.id,
                3: record.approval_d.id,
            }
            seq = record.approval_sec
            pre_seq = seq - 1 if seq > 0 else seq
            previous_approval = data_dict[pre_seq] if seq > 0 else False
            if (record.purchasing_group_rel == 'Buyer HO' and seq > 3) or\
                    (record.purchasing_group_rel != 'Buyer HO' and seq > 2):
                record.next_approval = False
                record.user_eligibility_release = False
                record.user_eligibility_unrelease = previous_approval == self.env.user.id
            else:
                record.next_approval = data_dict[seq]
                record.user_eligibility_release = record.next_approval == self.env.user
                record.user_eligibility_unrelease = previous_approval == self.env.user.id

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
            if checked:
                if (self.purchasing_group_rel == 'Buyer HO' and seq == 3) or\
                        (self.purchasing_group_rel != 'Buyer HO' and seq == 2):
                    self.write({'state': 'done'})
                if seq == 0:
                    self.approval_a_time = fields.Datetime.now()
                elif seq == 1:
                    self.approval_b_time = fields.Datetime.now()
                elif seq == 2:
                    self.approval_c_time = fields.Datetime.now()
                elif seq == 3:
                    self.approval_d_time = fields.Datetime.now()
                seq += 1
                self.approval_sec = seq
                return {}
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
                if seq == 0:
                    self.approval_a_time = False
                    self.write({'state': 'draft'})
                elif seq == 1:
                    self.approval_b_time = False
                elif seq == 2:
                    self.approval_c_time = False
                elif seq == 3:
                    self.approval_d_time = False
                return {}
            else:
                raise UserError('Anda tidak memiliki hak untuk unrelease!')
        else:
            raise UserError('Data belum ada melakukan release!')

    @api.model
    def create(self, vals):
        if 'order_line' not in vals.keys():
            raise UserError('Data produk tidak ditemukan!')
        else:
            return super(PurchaseOrder, self).create(vals)

    def write(self, vals):
        if vals.get('order_line'):
            if len(vals['order_line']) == 1:
                if (vals['order_line'][0][2] == False):
                    raise UserError('Data produk tidak ditemukan!')
        else:
            return super(PurchaseOrder, self).write(vals)
