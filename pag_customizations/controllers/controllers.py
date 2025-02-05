# -*- coding: utf-8 -*-
# from odoo import http


# class PagCustomizations(http.Controller):
#     @http.route('/pag_customizations/pag_customizations', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pag_customizations/pag_customizations/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pag_customizations.listing', {
#             'root': '/pag_customizations/pag_customizations',
#             'objects': http.request.env['pag_customizations.pag_customizations'].search([]),
#         })

#     @http.route('/pag_customizations/pag_customizations/objects/<model("pag_customizations.pag_customizations"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pag_customizations.object', {
#             'object': obj
#         })

