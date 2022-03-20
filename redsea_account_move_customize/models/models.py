# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', required=False ,
                                          index=True)
