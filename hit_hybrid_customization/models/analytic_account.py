
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class AccountAnalyticGroup(models.Model):
    _inherit = 'account.analytic.group'

    site_id = fields.Many2one('md.site', string='Site')



class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    site_id = fields.Many2one('md.site', string='Site', related='group_id.site_id')

    


    

