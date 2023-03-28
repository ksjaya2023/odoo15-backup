# -*- coding: utf-8 -*-
# from odoo import http


# class HitPurchaseOrderApproval(http.Controller):
#     @http.route('/hit_purchase_order_approval/hit_purchase_order_approval/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hit_purchase_order_approval/hit_purchase_order_approval/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hit_purchase_order_approval.listing', {
#             'root': '/hit_purchase_order_approval/hit_purchase_order_approval',
#             'objects': http.request.env['hit_purchase_order_approval.hit_purchase_order_approval'].search([]),
#         })

#     @http.route('/hit_purchase_order_approval/hit_purchase_order_approval/objects/<model("hit_purchase_order_approval.hit_purchase_order_approval"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hit_purchase_order_approval.object', {
#             'object': obj
#         })
