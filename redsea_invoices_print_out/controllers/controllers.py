# -*- coding: utf-8 -*-
# from odoo import http


# class RedseaInvoicesPrintOut(http.Controller):
#     @http.route('/redsea_invoices_print_out/redsea_invoices_print_out/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/redsea_invoices_print_out/redsea_invoices_print_out/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('redsea_invoices_print_out.listing', {
#             'root': '/redsea_invoices_print_out/redsea_invoices_print_out',
#             'objects': http.request.env['redsea_invoices_print_out.redsea_invoices_print_out'].search([]),
#         })

#     @http.route('/redsea_invoices_print_out/redsea_invoices_print_out/objects/<model("redsea_invoices_print_out.redsea_invoices_print_out"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('redsea_invoices_print_out.object', {
#             'object': obj
#         })
