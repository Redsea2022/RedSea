# -*- coding: utf-8 -*-
# from odoo import http


# class JournalEntriesDebitTotal(http.Controller):
#     @http.route('/journal_entries_debit_total/journal_entries_debit_total/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/journal_entries_debit_total/journal_entries_debit_total/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('journal_entries_debit_total.listing', {
#             'root': '/journal_entries_debit_total/journal_entries_debit_total',
#             'objects': http.request.env['journal_entries_debit_total.journal_entries_debit_total'].search([]),
#         })

#     @http.route('/journal_entries_debit_total/journal_entries_debit_total/objects/<model("journal_entries_debit_total.journal_entries_debit_total"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('journal_entries_debit_total.object', {
#             'object': obj
#         })
