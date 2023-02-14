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

    active = fields.Boolean(string='Active', default=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    name = fields.Char('Name')
    service_package_id = fields.Many2one(comodel_name='service.package')
    price = fields.Monetary('Price')
    product = fields.Many2one(comodel_name='product.product', string='Product')
    quantity = fields.Integer(string='Quantity')
    sequence = fields.Integer(string='Sequence')
    service_type = fields.Char(string='Service Type')  # related
    total_price = fields.Monetary('Total Price')  # compute
    unit_model = fields.Char(string='Unit Model')  # related
    uom_id = fields.Many2one(comodel_name='uom.uom', string='UoM')  # related
