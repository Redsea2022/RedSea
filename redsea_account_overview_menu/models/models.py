# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class ResUsers(models.Model):
    _inherit = 'res.users'

    journal_ids = fields.Many2many(comodel_name="account.journal", string="Journals")


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    def return_journal_with_domain(self):
        kanban_view = self.env.ref('account.account_journal_dashboard_kanban_view')
        user = self.env.user
        return {
            'name': _('Accounting Overview'),
            'view_mode': 'kanban, form',
            'res_model': 'account.journal',
            'usage': 'menu',
            'context': {'search_default_dashboard': 1},
            'domain': [('id', 'in', user.journal_ids.ids)],
            'view_id': False,
            'views': [
                (kanban_view.id, 'kanban'),
            ],
            'type': 'ir.actions.act_window',
        }
