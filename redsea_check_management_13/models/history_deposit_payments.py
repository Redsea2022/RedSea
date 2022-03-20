# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class HistoryDepositPayments(models.Model):
    _name = 'history.deposit.payments'

    deposit_id = fields.Many2one(comodel_name='account.batch.payment')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
    check_number = fields.Char(string='Received Check Number')
    bank_name = fields.Char(string='Bank Name')
    amount = fields.Monetary(string='Payment Amount')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    payment_date = fields.Date(string='Payment Date')
    due_date = fields.Date(string='Due Date')
    ref_coll_batch = fields.Date(string='Refund/Collect Date')
    multi_select = fields.Boolean(string='Multi Select')
    communication = fields.Char(string='Memo')
