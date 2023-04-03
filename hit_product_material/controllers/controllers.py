# -*- coding: utf-8 -*-
# from odoo import http


# class HitProductMaterial(http.Controller):
#     @http.route('/hit_product_material/hit_product_material/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hit_product_material/hit_product_material/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hit_product_material.listing', {
#             'root': '/hit_product_material/hit_product_material',
#             'objects': http.request.env['hit_product_material.hit_product_material'].search([]),
#         })

#     @http.route('/hit_product_material/hit_product_material/objects/<model("hit_product_material.hit_product_material"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hit_product_material.object', {
#             'object': obj
#         })
