# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('to_be_approved', 'To Be Approved'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ])
