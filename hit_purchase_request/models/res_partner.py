# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_COMODITY = [('explosives', 'Explosives'),
             ('production_equipment', 'Production Equipment')]

_SUPPLIER = [('manufacture_or_fabrication',
              'Manufacture or Fabrication'), ('distributor', 'Distributor')]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    certificated_no = fields.Char('Certificated No.')
    comodity_group_code = fields.Selection(
        string='Comodity Group Code', selection=_COMODITY)
    company_director = fields.Char('Company Director ')
    credit_limit_value = fields.Char('Credit Limit Value')
    turn_on_per_year = fields.Char('Turn On per Year')
    fax = fields.Char('Fax')
    holding_company_group = fields.Char('Holding Company Group')
    iso_company = fields.Char('ISO Company')
    supplier_type = fields.Selection(
        string='Supplier Type', selection=_SUPPLIER)
    main_product_ids = fields.One2many(
        'vendor.main.product', 'partner_id', string='Main Product / Brand Supplier')
    product_ids = fields.One2many(
        'vendor.product', 'partner_id', string='Product / Brand Supply To')
    others_product_ids = fields.One2many(
        'vendor.others.product', 'partner_id', string='Others Product & Brand From Supplier')
    business_reference_ids = fields.One2many(
        'vendor.business.reference', 'partner_id', string='Business References')


class VendorMainProduct(models.Model):
    _name = 'vendor.main.product'
    _description = 'Vendor Main Product Line'

    name = fields.Char('Main Product')
    sequence = fields.Integer('Sequence')
    partner_id = fields.Many2one('res.partner', string='Partner')


class VendorProduct(models.Model):
    _name = 'vendor.product'
    _description = 'Vendor Product Line'

    name = fields.Char('Product')
    sequence = fields.Integer('Sequence')
    partner_id = fields.Many2one('res.partner', string='Partner')


class VendorOthersProduct(models.Model):
    _name = 'vendor.others.product'
    _description = 'Vendor Others Product Line'

    name = fields.Char('Others Product')
    sequence = fields.Integer('Sequence')
    partner_id = fields.Many2one('res.partner', string='Partner')


class VendorBusinessReference(models.Model):
    _name = 'vendor.business.reference'
    _description = 'Vendor Business Reference Line'

    name = fields.Char('Business')
    sequence = fields.Integer('Sequence')
    partner_id = fields.Many2one('res.partner', string='Partner')
