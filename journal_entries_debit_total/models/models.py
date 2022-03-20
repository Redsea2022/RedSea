# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('line_ids')
    def get_total_debit(self):
        for rec in self:
            debit_total = sum(rec.line_ids.filtered(lambda line: line.amount_currency > 0).mapped('amount_currency'))
            print(debit_total)
            rec.debit_total = debit_total

    debit_total = fields.Float(string="Debit Total", compute='get_total_debit')

