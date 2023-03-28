# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class hit_tpe_migration(models.Model):
#     _name = 'hit_tpe_migration.hit_tpe_migration'
#     _description = 'hit_tpe_migration.hit_tpe_migration'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
