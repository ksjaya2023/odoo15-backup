from odoo import _, api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    act_hm = fields.Char(string='Actual HM')  # compute
    act_serv_date = fields.Date(string='Actual Service Date')  # compute
    attachment = fields.Char(string='Related to x_eqp_attachment')
    attachment_product = fields.Char(
        string='Related to x_eqp_attachment_produ')
    attachment_serial_no = fields.Char(string='Attachment Serial No.')
    estimasi_service_HRM = fields.Char(string='Estimasi Service HRM')
    curr_hrm_date = fields.Datetime(string='Current HRM Date')  # compute
    current_hrm = fields.Char(string='Current HRM')  # compute
    eqp_type = fields.Char(string='EQP Type')  # related
    height_cm = fields.Float(string='Height (cm)')
    length_cm = fields.Float(string='Length (cm)')
    lifetime = fields.Float(string='Lifetime')  # compute
    location = fields.Char(string='Location')
    plan_serv_hm = fields.Char(string='Plan Service HM')  # compute
    prev_serv_date = fields.Date(string='Previous Service Date')  # compute
    prev_serv_hrm = fields.Char(string='Previous Service HRM')  # compute
    production_year = fields.Char(string='Production Year')
    service_type = fields.Char(string='Service Type')  # compute
    # transfer = fields.Many2one(comodel_name='stock.picking', string='Transfer')
    weight_ton = fields.Float(string='Weight (ton)')
    width_cm = fields.Float(string='Width (cm)')
