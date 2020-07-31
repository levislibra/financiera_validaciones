# -*- coding: utf-8 -*-
from openerp import http

# class FinancieraValidaciones(http.Controller):
#     @http.route('/financiera_validaciones/financiera_validaciones/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/financiera_validaciones/financiera_validaciones/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('financiera_validaciones.listing', {
#             'root': '/financiera_validaciones/financiera_validaciones',
#             'objects': http.request.env['financiera_validaciones.financiera_validaciones'].search([]),
#         })

#     @http.route('/financiera_validaciones/financiera_validaciones/objects/<model("financiera_validaciones.financiera_validaciones"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('financiera_validaciones.object', {
#             'object': obj
#         })