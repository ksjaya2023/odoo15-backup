from odoo import _, api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    avatar_image = fields.Binary(string='Avatar Image')
    act_hm = fields.Char(string='Actual HM')  # compute
    act_serv_date = fields.Date(string='Actual Service Date')  # compute
    attachment_id = fields.Many2one('eqp.attachment', string='Attachment')
    attachment_product_id = fields.Many2one(
        'eqp.attachment.product', string='Attachment Product')
    attachment_serial_no = fields.Char(string='Attachment Serial No.')
    estimasi_service_HRM = fields.Char(string='Estimasi Service HRM')
    curr_hrm_date = fields.Datetime(string='Current HRM Date')  # compute
    current_hrm = fields.Char(string='Current HRM')  # compute
    height = fields.Float(string='Height')
    length = fields.Float(string='Length')
    lifetime = fields.Float(string='Lifetime')  # compute
    location = fields.Char(string='Location')
    engine_model_id = fields.Many2one('engine.model', string='Engine Model')
    brand_id = fields.Many2one('brand', string='Brand')
    unit_model_id = fields.Many2one('unit.model', string='Unit Model')
    status_id = fields.Many2one('eqp.status', string='Status')
    class_id = fields.Many2one('eqp.class', string='Class')
    eqp_type = fields.Char(
        string='EQP Type', related='class_id.description')  # related
    plan_serv_hm = fields.Char(string='Plan Service HM')  # compute
    prev_serv_date = fields.Date(string='Previous Service Date')  # compute
    prev_serv_hrm = fields.Char(string='Previous Service HRM')  # compute
    production_year = fields.Char(string='Production Year')
    service_type = fields.Char(string='Service Type')  # compute
    transfer = fields.Many2one(comodel_name='stock.picking', string='Transfer')
    weight = fields.Float(string='Weight')
    width = fields.Float(string='Width')
