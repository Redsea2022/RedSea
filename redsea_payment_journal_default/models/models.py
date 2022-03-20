# -*- coding: utf-8 -*-

from odoo import models, fields, api


class account_payment(models.Model):
    _inherit = "account.payment"

    @api.onchange('amount', 'currency_id')
    def _onchange_amount(self):
        jrnl_filters = self._compute_journal_domain_and_types()
        journal_types = jrnl_filters['journal_types']
        domain_on_types = [('type', 'in', list(journal_types))]
        if self.invoice_ids:
            domain_on_types.append(('company_id', '=', self.invoice_ids[0].company_id.id))
        # if self.journal_id.type not in journal_types or (self.invoice_ids and self.journal_id.company_id != self.invoice_ids[0].company_id):
        #     self.journal_id = self.env['account.journal'].search(domain_on_types + [('company_id', '=', self.env.company.id)], limit=1)
        return {'domain': {'journal_id': jrnl_filters['domain'] + domain_on_types}}
