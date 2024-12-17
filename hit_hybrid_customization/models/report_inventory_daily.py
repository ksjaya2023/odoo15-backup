from odoo import models, fields, api

class InventoryDailyMovement(models.Model):
    _name = 'inventory.daily.movement'
    _description = 'Inventory Daily Movement'
    _auto = False

    transaction_date = fields.Date(string='Transaction Date')
    product_id = fields.Many2one('product.product', string='Product')
    product_name = fields.Char(string='Product Name')
    location_id = fields.Many2one('stock.location', string='Location')
    location_name = fields.Char(string='Location Name')
    incoming_quantity = fields.Float(string='Incoming Quantity')
    outgoing_quantity = fields.Float(string='Outgoing Quantity')
    total = fields.Float(string='Total Movement')

    def init(self):
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW inventory_daily_movement AS (
                SELECT 
                    row_number() OVER () AS id,
                    DATE(date) AS transaction_date,
                    product_id,
                    product_name,
                    location_id,
                    location_name,
                    SUM(CASE 
                        WHEN destination_usage = 'internal' AND source_usage != 'internal' THEN qty_done 
                        WHEN destination_usage = 'internal' AND source_usage = 'internal' THEN qty_done 
                        ELSE 0 
                    END) AS incoming_quantity, 
                    SUM(CASE 
                        WHEN source_usage = 'internal' AND destination_usage != 'internal' THEN qty_done 
                        WHEN source_usage = 'internal' AND destination_usage = 'internal' THEN qty_done 
                        ELSE 0 
                    END) AS outgoing_quantity,
                    SUM(CASE 
                        WHEN destination_usage = 'internal' AND source_usage != 'internal' THEN qty_done 
                        WHEN destination_usage = 'internal' AND source_usage = 'internal' THEN qty_done 
                        ELSE 0 
                    END) 
                    - SUM(CASE 
                        WHEN source_usage = 'internal' AND destination_usage != 'internal' THEN qty_done 
                        WHEN source_usage = 'internal' AND destination_usage = 'internal' THEN qty_done 
                        ELSE 0 
                    END) AS total
                FROM (
                    SELECT
                        product_moves.date,
                        product_moves.product_id,
                        pt.name AS product_name,
                        product_moves.location_id AS source_location,
                        product_moves.location_dest_id AS destination_location,
                        location.usage AS source_usage,
                        dest_location.usage AS destination_usage,
                        product_moves.qty_done,
                        product_moves.location_dest_id AS location_id,
                        dest_location.complete_name AS location_name
                    FROM stock_move_line product_moves
                    JOIN stock_location location ON product_moves.location_id = location.id
                    JOIN stock_location dest_location ON product_moves.location_dest_id = dest_location.id
                    JOIN product_product pp ON product_moves.product_id = pp.id
                    JOIN product_template pt ON pp.product_tmpl_id = pt.id
                    WHERE state = 'done'
                ) AS movements
                GROUP BY transaction_date, product_id, product_name, location_id, location_name
                ORDER BY transaction_date, product_id, location_id
            )
        """)