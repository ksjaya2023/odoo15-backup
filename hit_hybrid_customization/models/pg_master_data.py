
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PGMDSite(models.Model):
    _name = 'md.site'
    _description = 'Site Master Data'

    name = fields.Char("Site", required=True)
    active = fields.Boolean("Active", default=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    is_default = fields.Boolean('Default')

    
