from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    @api.model
    def create(self, vals):
        # _logger.error('###############')
        # _logger.error(vals)
        if 'product_qty' in vals:
            del vals['product_qty']
        return super(StockMove, self).create(vals)

    # @api.model
    # def write(self, vals):
    #     # _logger.error('###############')
    #     # _logger.error(vals)
    #     if 'product_qty' in vals:
    #         del vals['product_qty']
    #     return super(StockMove, self).write(vals)

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    @api.model
    def create(self, vals):
        # _logger.error('###############')
        # _logger.error(vals)
        if 'product_qty' in vals:
            del vals['product_qty']
        return super(StockMoveLine, self).create(vals)

    @api.model
    def write(self, vals):
        # _logger.error('###############')
        # _logger.error(vals)
        if 'product_qty' in vals:
            del vals['product_qty']
        return super(StockMoveLine, self).write(vals)