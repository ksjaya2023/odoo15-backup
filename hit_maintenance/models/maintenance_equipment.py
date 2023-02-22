from odoo import _, api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    avatar_image = fields.Binary(string='Avatar Image')
    act_hm = fields.Char(string='Actual HM', compute='_compute_act_hm')
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
    prev_serv_hrm = fields.Char(
        string='Previous Service HRM', compute='_compute_prev_serv_hrm')
    production_year = fields.Char(string='Production Year')
    service_type = fields.Char(string='Service Type')  # compute
    transfer = fields.Many2one(comodel_name='stock.picking', string='Transfer')
    weight = fields.Float(string='Weight')
    width = fields.Float(string='Width')

    @api.depends('prev_serv_hrm')
    def _compute_prev_serv_hrm(self):
        for record in self:
            previous_hrm = 0
            current_hrm = 0

            # Get Last HRM
            hms = record.env['measuring.equipment'].search(
                [('equipment_id', '=', record.id)], order='measuring_date desc', limit=1)
            if hms:
                for hm in hms:
                    current_hrm = hm.hourmeter
                    break
            list_service_types = record.env['service.type'].search(
                [], order='service_amount asc')
            if list_service_types:
                if current_hrm:
                    value = 0
                    mod = 0
                    previous_hrm = 0
                    service_hrm = 0
                    while service_hrm < current_hrm:
                        for list_type in list_service_types:
                            if list_type.service_amount > 1000:
                                continue
                            service_hrm = value + list_type.service_amount
                            if (service_hrm > current_hrm):
                                break
                            else:
                                previous_hrm = list_type.service_amount
                            # Check modulus by 1000
                            mod = list_type.service_amount % 1000
                            if (mod == 0):
                                value = value + 1000
            record.prev_serv_hrm = str(previous_hrm)

    @api.depends('act_hm')
    def _compute_act_hm(self):
        for record in self:
            current_hrm = 0
            i = 0
            hms = record.env['measuring.equipment'].search(
                [('equipment_id', '=', record.id)], order='measuring_date desc', limit=1)
            if hms:
                for hm in hms:
                    if (i == 0):
                        current_hrm = hm.hourmeter
                        i = 1
            record.act_hm = str(current_hrm)
