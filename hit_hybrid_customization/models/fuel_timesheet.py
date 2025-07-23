from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    created_from_fuel_timesheet = fields.Boolean(string="Created From Timesheet")
    remarks = fields.Char(string="Remarks")

class StockMove(models.Model):
    _inherit = 'stock.move'

    description_fuel_timesheet = fields.Char(string="Description")

    # function untuk tidak merge stock.move, distinct berdasarkan description dari fuel timesheet
    def _prepare_merge_moves_distinct_fields(self):
        distinct_fields = super(StockMove, self)._prepare_merge_moves_distinct_fields()
        distinct_fields.append('description_fuel_timesheet')
        return distinct_fields

class HITFuelTimesheet(models.Model):
    _name = 'hit.fuel.timesheet'
    _description = 'HIT Fuel Timesheet'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    month_list = [
        ('january', 'January'),
        ('february', 'February'),
        ('march', 'March'),
        ('april', 'April'),
        ('may', 'May'),
        ('june', 'June'),
        ('july', 'July'),
        ('august', 'August'),
        ('september', 'September'),
        ('october', 'October'),
        ('november', 'November'),
        ('december', 'December'),
    ]

    shift_list = [
        ('day', 'Day'),
        ('night', 'Night'),
    ]

    fuel_date = fields.Date(string="Tanggal Fuel Issued")
    fuel_month = fields.Selection(month_list,string="Bulan Fuel Issued")
    fuel_year = fields.Char(string="Tahun Fuel Issued")
    fuel_shift = fields.Selection(shift_list,string="Shift Fuel Issued")
    equipment_id = fields.Many2one('maintenance.equipment',string="Unit ID")
    equipment_egi = fields.Char(string="EGI")
    x_studio_analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string="Analytic Account",
        related='equipment_id.x_studio_analytic_account',
        store=True
    )
    owner_user_id = fields.Many2one(
        'res.partner',
        string="Owner",
        related='equipment_id.x_studio_owner',
        store=True
    )
    location_id = fields.Many2one('stock.location',string="Source Location")
    picking_type_id = fields.Many2one('stock.picking.type', string="Operation Type", compute='_compute_picking_type_and_dest', store=True)
    location_dest_id = fields.Many2one('stock.location', string="Destination Location", compute='_compute_picking_type_and_dest', store=True)
    alocation = fields.Char(string="Alokasi")
    mining_alocation = fields.Char(string="RAW Mining Alokasi")
    hrm_alocation = fields.Char(string="RAW HRM Alokasi")
    equip_capacity = fields.Integer(string="Kapasitas Fuel Tank")
    fbr_budget = fields.Integer(string="FBR Budget")
    fuel_issued = fields.Integer(string="Quantity Liter")
    hm_km = fields.Char(string="HM/KM")
    stock_picking_id = fields.Many2one('stock.picking',string="GI Document")
    state = fields.Selection(related='stock_picking_id.state', store=True, readonly=False)
    revision = fields.Integer(string="Revision")

    @api.model_create_multi
    def create(self, vals_list):
        seen_keys = set()
        for vals in vals_list:
            date = vals.get('fuel_date')
            unit = vals.get('equipment_id')
            shift = vals.get('fuel_shift')
            shift_label = dict(self._fields['fuel_shift'].selection).get(shift, shift)
            if date and unit and shift:
                key = (date, unit, shift)
                if key in seen_keys:
                    raise ValidationError(
                        f"Duplicate entry detected within imported data: Unit ID {unit}, Date {date}, Shift {shift_label}."
                    )
                seen_keys.add(key)
                exists = self.search([
                    ('fuel_date', '=', date),
                    ('equipment_id', '=', unit),
                    ('fuel_shift', '=', shift)
                ], limit=1)
                if exists:
                    raise ValidationError(
                        f"Duplicate entry already exists in database for Unit ID {unit}, Date {date}, Shift {shift_label}."
                    )
        return super().create(vals_list)

    @api.onchange('fuel_date')
    def _onchange_fuel_date(self):
        if self.fuel_date:
            month_index = self.fuel_date.month - 1
            self.fuel_month = self.month_list[month_index][0]
            self.fuel_year = self.fuel_date.year

    @api.depends('location_id')
    def _compute_picking_type_and_dest(self):
        for rec in self:
            rec.picking_type_id = False
            rec.location_dest_id = False
            if rec.location_id:
                picking_type = self.env['stock.picking.type'].search([
                    ('default_location_src_id', '=', rec.location_id.id),
                    ('sequence_code','=','OUT'),
                ], limit=1)
                if picking_type:
                    rec.picking_type_id = picking_type.id
                    rec.location_dest_id = picking_type.default_location_dest_id.id

    def create_gi(self):
        today = fields.Date.context_today(self)
        current_month, current_year = today.month, today.year
        
        invalid_records = self.filtered(lambda r: not r.fuel_date or r.fuel_date.month != current_month or r.fuel_date.year != current_year)
        if invalid_records:
            raise UserError(f"Fuel Timesheet must be in the same month as {today.strftime('%B %Y')}.")
        
        location_ids = set(self.mapped('location_id.id'))
        if len(location_ids) > 1:
            raise UserError("Fuel Timesheet must have the same Location.")
        
        existing_pickings = self.filtered(lambda r: r.stock_picking_id and r.stock_picking_id.state != 'cancel')
        if existing_pickings:
            raise UserError("GI document already exists for this Fuel Timesheet.")
        
        records_to_update = self.filtered('stock_picking_id')
        if records_to_update:
            for rec in records_to_update:
                rec.revision = (rec.revision or 0) + 1
        
        # Cache location_id (ambil dari set yang sudah ada)
        location_id = next(iter(location_ids))
        
        product = self.env['product.product'].search([('name', '=', '[FUEL] Fuel')], limit=1)
        if not product:
            raise UserError("Product '[FUEL] Fuel' not found.\nPlease create this product first")
        
        first_record = self[0]
        picking_type_id = first_record.picking_type_id.id
        location_dest_id = first_record.location_dest_id.id
        
        move_lines = [
            (0, 0, {
                'name': 'Fuel Timesheet',
                'location_id': location_id,
                'location_dest_id': rec.location_dest_id.id,
                'analytic_account_id': rec.x_studio_analytic_account_id.id,
                'product_id': product.id,
                'description_fuel_timesheet': f'Fuel Consumed {rec.fuel_date} {rec.equipment_id.x_studio_equipment_name}',
                'product_uom': product.uom_id.id,
                'product_uom_qty': rec.fuel_issued,
                'quantity_done': rec.fuel_issued,
                'qty_done': rec.fuel_issued,
            })
            for rec in self
        ]
        picking = self.env['stock.picking'].create({
            'move_ids_without_package': move_lines,
            'created_from_fuel_timesheet': True,
            'picking_type_id': picking_type_id,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
        })
        
        # for move in picking.move_ids_without_package:
        #     move.qty_done = move.product_uom_qty
        
        self.write({'stock_picking_id': picking.id})
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'res_id': picking.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_stock_picking(self):
        self.ensure_one()
        if not self.stock_picking_id:
            raise UserError("No GI Document linked!")
        return {
            'type': 'ir.actions.act_window',
            'name': 'GI Document',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'res_id': self.stock_picking_id.id,
            'target': 'current',
        }

    # def create_gi(self):
    #     move_lines = []
    #     for record in self:
    #         move_lines.append((0, 0, {
    #             'location_id': record.location_id.id,
    #             'analytic_account_id': record.x_studio_analytic_account_id.id,
    #         }))
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'stock.picking',
    #         'view_mode': 'form',
    #         'target': 'current',
    #         'context': {
    #             'default_move_ids_without_package': move_lines,
    #             'default_fuel_timesheet_ids': self.ids,
    #         }
    #     }