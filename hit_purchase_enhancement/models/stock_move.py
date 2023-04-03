from odoo import api, fields, models


class StockMove(models.Model):
  _inherit = "stock.move"

  def _get_price_unit(self):
    """ 
    Returns the unit price to value this stock move
    FYI:
      Kodenya sama persis dengan di stock_account.
      Ga tau kenapa harus ditulis methodnya di sini, 
      tapi kalau ga ada freight costnya ga kehitung.
    """
    self.ensure_one()
    price_unit = self.price_unit
    # If the move is a return, use the original move's price unit.
    if self.origin_returned_move_id and self.origin_returned_move_id.sudo().stock_valuation_layer_ids:
      price_unit = self.origin_returned_move_id.stock_valuation_layer_ids[-1].unit_cost
    return not self.company_id.currency_id.is_zero(price_unit) and price_unit or self.product_id.standard_price