# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_MEASURING_TYPE = [('Hourmeter', 'Hourmeter'),
                   ('Odometer', 'Odometer')
                   ]


class MeasuringEquipment(models.Model):
    _name = 'measuring.equipment'
    _description = 'Measuring Equipment'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char('Name')
    sequence = fields.Integer('Sequence')
    create_wo = fields.Boolean('Create WO')
    current_hm = fields.Integer(
        'Current HM', help='Current value of Hourmeter.')
    delta = fields.Integer('Delta')
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment')
    hm_awal = fields.Integer(
        'HM Awal', help='Begin value of Hourmeter.')  # compute
    hourmeter = fields.Integer(
        'Hourmeter Total', help='The Total Computation of Hourmeter.')
    measuring_date = fields.Date('Measuring Date')
    measuring_type = fields.Selection(
        selection=_MEASURING_TYPE, string='measuring_type')
    reset = fields.Boolean(
        'Reset', help='True if the hour meter finished a cycle.')
    sisa_serv_type = fields.Char('Sisa Service Type')
    test_hm_awal = fields.Integer('Test HM Awal')
    work_order_id = fields.Many2one('maintenance.request', string='Work Order')
