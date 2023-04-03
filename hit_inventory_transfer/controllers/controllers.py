# -*- coding: utf-8 -*-
# from odoo import http


# class HitInventoryTransfer(http.Controller):
#     @http.route('/hit_inventory_transfer/hit_inventory_transfer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hit_inventory_transfer/hit_inventory_transfer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hit_inventory_transfer.listing', {
#             'root': '/hit_inventory_transfer/hit_inventory_transfer',
#             'objects': http.request.env['hit_inventory_transfer.hit_inventory_transfer'].search([]),
#         })

#     @http.route('/hit_inventory_transfer/hit_inventory_transfer/objects/<model("hit_inventory_transfer.hit_inventory_transfer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hit_inventory_transfer.object', {
#             'object': obj
#         })
