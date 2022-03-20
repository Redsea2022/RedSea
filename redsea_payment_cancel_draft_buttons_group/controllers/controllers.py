# -*- coding: utf-8 -*-
# from odoo import http


# class RedseaPaymentCancelDraftButtonsGroup(http.Controller):
#     @http.route('/redsea_payment_cancel_draft_buttons_group/redsea_payment_cancel_draft_buttons_group/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/redsea_payment_cancel_draft_buttons_group/redsea_payment_cancel_draft_buttons_group/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('redsea_payment_cancel_draft_buttons_group.listing', {
#             'root': '/redsea_payment_cancel_draft_buttons_group/redsea_payment_cancel_draft_buttons_group',
#             'objects': http.request.env['redsea_payment_cancel_draft_buttons_group.redsea_payment_cancel_draft_buttons_group'].search([]),
#         })

#     @http.route('/redsea_payment_cancel_draft_buttons_group/redsea_payment_cancel_draft_buttons_group/objects/<model("redsea_payment_cancel_draft_buttons_group.redsea_payment_cancel_draft_buttons_group"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('redsea_payment_cancel_draft_buttons_group.object', {
#             'object': obj
#         })
