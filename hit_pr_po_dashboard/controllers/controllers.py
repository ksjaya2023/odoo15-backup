# -*- coding: utf-8 -*-
# from odoo import http


# class HitDashboardReport(http.Controller):
#     @http.route('/hit_dashboard_report/hit_dashboard_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hit_dashboard_report/hit_dashboard_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hit_dashboard_report.listing', {
#             'root': '/hit_dashboard_report/hit_dashboard_report',
#             'objects': http.request.env['hit_dashboard_report.hit_dashboard_report'].search([]),
#         })

#     @http.route('/hit_dashboard_report/hit_dashboard_report/objects/<model("hit_dashboard_report.hit_dashboard_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hit_dashboard_report.object', {
#             'object': obj
#         })
