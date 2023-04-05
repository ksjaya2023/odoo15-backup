# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountAsset(models.Model):
    _inherit = 'account.asset'
    _description = 'account.asset'

    def name_get(self):
        result = []
        for record in self:
            if record.name and record.x_studio_asset_description:
                result.append((record.id, record.name + '/' +
                              record.x_studio_asset_description))
            if record.name and not record.x_studio_asset_description:
                result.append((record.id, record.name))
        return result
