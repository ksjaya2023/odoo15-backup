# -*- coding: utf-8 -*-
# from odoo import http


# class HitTpeMigration(http.Controller):
#     @http.route('/hit_tpe_migration/hit_tpe_migration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hit_tpe_migration/hit_tpe_migration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hit_tpe_migration.listing', {
#             'root': '/hit_tpe_migration/hit_tpe_migration',
#             'objects': http.request.env['hit_tpe_migration.hit_tpe_migration'].search([]),
#         })

#     @http.route('/hit_tpe_migration/hit_tpe_migration/objects/<model("hit_tpe_migration.hit_tpe_migration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hit_tpe_migration.object', {
#             'object': obj
#         })
