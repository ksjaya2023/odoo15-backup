# -*- coding: utf-8 -*-
# from odoo import http


# class HitPurchaseMaster(http.Controller):
#     @http.route('/hit_purchase_master/hit_purchase_master/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hit_purchase_master/hit_purchase_master/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hit_purchase_master.listing', {
#             'root': '/hit_purchase_master/hit_purchase_master',
#             'objects': http.request.env['hit_purchase_master.hit_purchase_master'].search([]),
#         })

#     @http.route('/hit_purchase_master/hit_purchase_master/objects/<model("hit_purchase_master.hit_purchase_master"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hit_purchase_master.object', {
#             'object': obj
#         })
