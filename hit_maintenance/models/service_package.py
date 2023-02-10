from odoo import _, api, fields, models


class ServicePackage(models.Model):
    _name = 'service.package'
    _description = 'Service Package'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Package Name')
    # service_package = fields.Many2many(
    #     comodel_name='service.package', string='Service Package')  # related
    service_type_ids = fields.Many2many(
        comodel_name='service.type', string='Service Types')
    sequence = fields.Integer(string='sequence')
    service_type = fields.Many2one(
        comodel_name='service.type', string='Service Type')
    unit_model = fields.Many2one(
        comodel_name='unit.model', string='Unit Model')
    service_package_ids = fields.One2many(
        comodel_name='service.package.line', inverse_name='service_package_id', string='Service Item')


class ServicePackageLine(models.Model):
    _name = 'service.package.line'
    _description = 'Service Package Line'

    service_package_id = fields.Many2one(comodel_name='service.package')
