from odoo import _, api, fields, models


class ServicePackage(models.Model):
    _name = 'service.package'
    _description = 'Service Package'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Package Name', compute='_compute_name')
    service_type_ids = fields.Many2many(
        comodel_name='service.type', string='Service Types')
    sequence = fields.Integer(string='Sequence')
    service_type_id = fields.Many2one(
        comodel_name='service.type', string='Service Type', required=True)
    unit_model_id = fields.Many2one(
        comodel_name='unit.model', string='Unit Model', required=True)
    service_package_ids = fields.One2many(
        comodel_name='service.package.line', inverse_name='service_package_id', string='Service Item')

    @api.depends('unit_model_id', 'service_type_id')
    def _compute_name(self):
        for record in self:
            record.name = str(
                record.id) + '/' + str(record.unit_model_id.name) + '/' + str(record.service_type_id.name)


class ServicePackageLine(models.Model):
    _name = 'service.package.line'
    _description = 'Service Package Line'

    active = fields.Boolean(string='Active', default=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    name = fields.Char('Name')
    service_package_id = fields.Many2one(comodel_name='service.package')
    product_id = fields.Many2one(
        comodel_name='product.product', string='Product')
    price = fields.Float('Price', related='product_id.standard_price')
    quantity = fields.Integer(string='Quantity')
    sequence = fields.Integer(string='Sequence')
    service_type = fields.Char(
        string='Service Type', related='service_package_id.service_type_id.name')
    total_price = fields.Monetary(
        'Total Price', compute='_compute_total_price')  # compute
    unit_model = fields.Char(
        string='Unit Model', related='service_package_id.unit_model_id.name')
    uom_id = fields.Many2one(
        comodel_name='uom.uom', string='UoM', related='product_id.uom_id')

    @api.depends('quantity', 'price')
    def _compute_total_price(self):
        for record in self:
            prices = 0
            prices = record.quantity * record.price
            record.total_price = prices
