# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime


class MultiChecks(models.Model):
    _name = 'multi.checks'

    name = fields.Char(readonly=True)
    payment_journal = fields.Many2one(comodel_name='account.journal', string='Payment Journal', required=True,
                                      domain=[('type', 'in', ['bank', 'cash']), ('is_notes_receivable', '=', True)])
    payment_date = fields.Date(string='Payment Date', required=True)
    ref = fields.Char(string='Reference')
    payment_ids = fields.One2many(comodel_name='account.payment', inverse_name='multi_check_id', string='Checks')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted')], default='draft')

    @api.onchange('payment_ids', 'payment_journal', 'payment_date')
    def get_payment_fields(self):
        for rec in self:
            for line in rec.payment_ids:
                line.payment_method_id = 4
                line.journal_id = rec.payment_journal.id
                line.payment_date = rec.payment_date

    def padding_calc(self, num):
        padding = ''
        padding_size = 5 - len(str(num))
        if padding_size > 0:
            while (padding_size):
                padding = padding + '0'
                padding_size = padding_size - 1
        return padding + str(num)

    # #@api.multi
    def get_checks_posted(self):
        for line in self.payment_ids:
            if line.state == 'draft':
                line.post()

        current_year = int(datetime.today().year)
        year_obj = self.env['multi.checks.sequence'].search([('seq_year', '=', current_year)])
        if year_obj:
            self.name = 'Multi Checks/' + str(current_year) + '/' + self.padding_calc(year_obj.seq)
            year_obj.seq = year_obj.seq + 1

        else:
            self.name = 'Multi Checks/' + str(current_year) + '/' + '00001'
            year_obj.create({
                'seq': 2, 'seq_year': current_year
            })
        self.state = 'posted'
