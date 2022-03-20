# -*- coding: utf-8 -*-
# from odoo import http


# class RedseaAccountMoveAskReview(http.Controller):
#     @http.route('/redsea_account_move_ask_review/redsea_account_move_ask_review/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/redsea_account_move_ask_review/redsea_account_move_ask_review/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('redsea_account_move_ask_review.listing', {
#             'root': '/redsea_account_move_ask_review/redsea_account_move_ask_review',
#             'objects': http.request.env['redsea_account_move_ask_review.redsea_account_move_ask_review'].search([]),
#         })

#     @http.route('/redsea_account_move_ask_review/redsea_account_move_ask_review/objects/<model("redsea_account_move_ask_review.redsea_account_move_ask_review"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('redsea_account_move_ask_review.object', {
#             'object': obj
#         })
