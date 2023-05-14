from operator import mod
from odoo import api, fields, models


class MaterialType(models.Model):
    _name = "material.type"
    _description = "Material Type"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")


class MaterialGroup(models.Model):
    _name = "material.group"
    _description = "Material Group"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
