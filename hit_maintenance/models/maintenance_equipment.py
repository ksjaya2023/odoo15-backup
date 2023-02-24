from odoo import _, api, fields, models, exceptions
import datetime


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    avatar_image = fields.Binary(string='Avatar Image')
    act_hm = fields.Char(string='Actual HM', compute='_compute_act_hm')
    act_serv_date = fields.Date(
        string='Actual Service Date', compute='_compute_act_serv_date')
    attachment_id = fields.Many2one('eqp.attachment', string='Attachment')
    attachment_product_id = fields.Many2one(
        'eqp.attachment.product', string='Attachment Product')
    attachment_serial_no = fields.Char(string='Attachment Serial No.')
    estimasi_service_HRM = fields.Char(string='Estimasi Service HRM')
    curr_hrm_date = fields.Datetime(
        string='Current HRM Date', compute='_compute_curr_hrm_date')
    current_hrm = fields.Char(string='Current HRM',
                              compute='_compute_current_hrm')
    height = fields.Float(string='Height')
    length = fields.Float(string='Length')
    lifetime = fields.Float(string='Lifetime', compute='_compute_lifetime')
    location = fields.Char(string='Location')
    engine_model_id = fields.Many2one('engine.model', string='Engine Model')
    brand_id = fields.Many2one('brand', string='Brand')
    unit_model_id = fields.Many2one('unit.model', string='Unit Model')
    status_id = fields.Many2one('eqp.status', string='Status')
    class_id = fields.Many2one('eqp.class', string='Class')
    eqp_type = fields.Char(
        string='EQP Type', related='class_id.description')
    plan_serv_hm = fields.Char(
        string='Plan Service HM', compute='_compute_plan_serv_hm')
    prev_serv_date = fields.Date(
        string='Previous Service Date', compute='_compute_prev_serv_date')
    prev_serv_hrm = fields.Char(
        string='Previous Service HRM', compute='_compute_prev_serv_hrm')
    production_year = fields.Char(string='Production Year')
    service_type = fields.Char(
        string='Service Type', compute='_compute_service_type')
    transfer = fields.Many2one(comodel_name='stock.picking', string='Transfer')
    weight = fields.Float(string='Weight')
    width = fields.Float(string='Width')

    @api.constrains('production_year')
    def _check_production_year(self):
        for record in self:
            if record.production_year:
                year_range = False
                cek_numerik = record.production_year.isnumeric()
                if cek_numerik:
                    if int(record.production_year) > 1900 and int(record.production_year) < 3000:
                        year_range = True

                if not year_range:
                    raise exceptions.ValidationError(
                        "The production year cannot be earlier than 1900 and no later than 3000.")

    @api.depends('act_hm')
    def _compute_act_hm(self):
        for record in self:
            curr_hm = 0
            i = 0
            hm = record.env['measuring.equipment'].search(
                [('equipment_id', '=', record.id)], order='measuring_date desc')
            if hm:
                for line in hm:
                    if (i == 0):
                        curr_hm = line.hourmeter
                        i = 1
            record.act_hm = str(curr_hm)

    @api.depends('act_serv_date')
    def _compute_act_serv_date(self):
        for record in self:
            prev_date = None
            wo = record.env['maintenance.request'].search(
                [('equipment_id', '=', record.id)], order='schedule_date desc')
            if wo:
                i = 0
                for row_wo in wo:
                    i = i + 1
                    if i == 1:
                        prev_date = row_wo.schedule_date
                        record.act_serv_date = prev_date

    @api.depends('curr_hrm_date')
    def _compute_curr_hrm_date(self):
        for record in self:
            curr_date = datetime.date.today()
            hm = record.env['measuring.equipment'].search(
                [('equipment_id', '=', record.id)], order='measuring_date desc')
            if hm:
                i = 0
                for line in hm:
                    i = i + 1
                    if i == 1:
                        curr_date = line.measuring_date
            record.curr_hrm_date = curr_date

    @api.depends('current_hrm')
    def _compute_current_hrm(self):
        for record in self:
            curr_hm = 0
            i = 0
            hm = record.env['measuring.equipment'].search(
                [('equipment_id', '=', record.id)], order='measuring_date desc')
            if hm:
                for line in hm:
                    if (i == 0):
                        curr_hm = line.hourmeter
                        i = 1
            record.current_hrm = str(curr_hm)

    @api.depends('effective_date')
    def _compute_lifetime(self):
        for record in self:
            total_age = 0
            if record.effective_date:
                today_date = datetime.date.today()
                bdate = record.effective_date
                total_age = str((today_date - bdate).days / 365)
            record.lifetime = total_age

    @api.depends('plan_serv_hm')
    def _compute_plan_serv_hm(self):
        for record in self:
            curr_hm = 0
            serv_typ = 0
            # get HM terakhir
            hm = record.env['measuring.equipment'].search(
                [('equipment_id', '=', record.id)], order='measuring_date desc', limit=1)
            if hm:
                for line in hm:
                    curr_hm = line.hourmeter
                    break

            # get list service type
            fiel_list_type = record.env['service.type'].search(
                [], order='service_amount asc')
            if fiel_list_type:
                if curr_hm:
                    lt = 0
                    ribuan = 0
                    mod = 0

                    while lt < curr_hm:
                        for list_type in fiel_list_type:
                            if list_type.service_amount > 1000:
                                continue
                            lt = ribuan + list_type.service_amount
                            if (lt > curr_hm):
                                break
                            mod = list_type.service_amount % 1000
                            if (mod == 0):
                                ribuan = ribuan + 1000
                    serv_typ = lt
            else:
                for list_type in fiel_list_type:
                    serv_typ = list_type.service_amount
                    break
            record.plan_serv_hm = str(serv_typ)

    @api.depends('prev_serv_date')
    def _compute_prev_serv_date(self):
        for record in self:
            prev_date = None
            wo = record.env['maintenance.request'].search(
                [('equipment_id', '=', record.id)], order='schedule_date desc')
            if wo:
                i = 0
                for row_wo in wo:
                    i = i + 1
                    if i == 2:
                        prev_date = row_wo.schedule_date
            record.prev_serv_date = prev_date

    @api.depends('prev_serv_hrm')
    def _compute_prev_serv_hrm(self):
        for record in self:
            prev_hrm = 0
            curr_hm = 0
            # get HRM terakhir
            hm = record.env['measuring.equipment'].search(
                [('equipment_id', '=', record.id)], order='measuring_date desc', limit=1)
            if hm:
                for line in hm:
                    curr_hm = line.hourmeter
                    break
            fiel_list_type = record.env['service.type'].search(
                [], order='service_amount asc')
            if fiel_list_type:
                if curr_hm:
                    ribuan = 0
                    mod = 0
                    prev_hrm = 0
                    lt = 0
                    while lt < curr_hm:
                        for list_type in fiel_list_type:
                            if list_type.service_amount > 1000:
                                continue
                            lt = ribuan + list_type.service_amount
                            if (lt > curr_hm):
                                break
                            else:
                                prev_hrm = list_type.service_amount
                            # cek kelipatan seribu
                            mod = list_type.service_amount % 1000
                            if (mod == 0):
                                ribuan = ribuan + 1000
            record.prev_serv_hrm = str(prev_hrm)

    @api.depends('service_type')
    def _compute_service_type(self):
        for record in self:
            curr_hm = 0
            serv_typ = 0
            curr_serv = 0
            # get HM terakhir
            hm = record.env['measuring.equipment'].search(
                [('equipment_id', '=', record.id)], order='measuring_date desc', limit=1)
            if hm:
                for line in hm:
                    curr_hm = line.x_studio_hourmeter
                    break
            # get list service type
            fiel_list_type = record.env['service.type'].search(
                [], order='service_amount asc')
            if fiel_list_type:
                if curr_hm:
                    lt = 0
                    ribuan = 0
                    mod = 0
                    while lt < curr_hm:
                        for list_type in fiel_list_type:
                            if list_type.service_amount > 1000:
                                continue
                            lt = ribuan + list_type.service_amount
                            curr_serv = list_type.service_amount
                            if (lt > curr_hm):
                                break
                            mod = list_type.service_amount % 1000
                            if (mod == 0):
                                ribuan = ribuan + 1000
                    serv_typ = lt
            else:
                for list_type in fiel_list_type:
                    curr_serv = list_type.service_amount
                    break
            record['service_type'] = str(curr_serv)
