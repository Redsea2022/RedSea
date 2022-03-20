# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MakeApprovalWizard(models.TransientModel):
    _name = 'make.approval.wizard'

    review = fields.Selection(string="Review", selection=[('approve', 'Approve'), ('reject', 'Reject')], required=True)
    reason = fields.Text(string='Reason')

    def make_approval(self):
        login = self.env.user
        invoice = self.env['account.move'].browse(self.env.context.get('active_id'))
        for rec in self:
            if rec.review == 'approve':
                review = self.env['approval.log'].sudo().create({
                    'user_id': login.id,
                    'date': fields.Datetime.now(),
                    'state': 'Approved',
                    'reason': rec.reason,
                })
                invoice.write({
                    'log_ids': [(4, review.id)],
                    'state': 'approved'
                })
            else:
                review = self.env['approval.log'].sudo().create({
                    'user_id': login.id,
                    'date': fields.Datetime.now(),
                    'state': 'Rejected',
                    'reason': rec.reason,
                })
                invoice.write({
                    'log_ids': [(4, review.id)],
                    'state': 'rejected'
                })


class ApprovalLog(models.Model):
    _name = 'approval.log'
    _description = 'Approval Log'

    user_id = fields.Many2one(comodel_name="res.users", string="User")
    state = fields.Char(string="State")
    date = fields.Datetime(string="Date")
    reason = fields.Char(string="Reason")
    move_id = fields.Many2one(comodel_name="account.move")


class AccountMove(models.Model):
    _inherit = 'account.move'

    state = fields.Selection([('draft', 'Draft'), ('waiting', 'Waiting Review'), ('approved', 'Approved'),
                              ('rejected', 'Rejected'), ('posted', 'Posted'),
                              ('cancel', 'Cancelled')], string='Status', required=True, readonly=True, copy=False,
                             tracking=True, default='draft')

    log_ids = fields.One2many(comodel_name="approval.log", inverse_name="move_id", readonly=1)

    def ask_review(self):
        for rec in self:
            needaction_partner_ids = self.env.ref('redsea_account_move_ask_review.audit_group').users.mapped('partner_id')
            h = []
            o = self.env['mail.message'].search([('record_name', '!=', False), ('model', '=', 'account.move')],
                                                limit=1)
            for g in needaction_partner_ids:
                h.append((0, 0, {'mail_message_id': o.id, 'res_partner_id': g.id}))
            login_user = self.env.user
            if rec.type == 'out_invoice':
                action = self.env.ref('account.action_move_out_invoice_type').id
                menu = self.env.ref('account.menu_action_move_out_invoice_type').id
            elif rec.type == 'out_refund':
                action = self.env.ref('account.action_move_out_refund_type').id
                menu = self.env.ref('account.menu_action_move_out_refund_type').id
            elif rec.type == 'in_invoice':
                action = self.env.ref('account.action_move_in_invoice_type').id
                menu = self.env.ref('account.menu_action_move_in_invoice_type').id
            elif rec.type == 'in_refund':
                action = self.env.ref('account.action_move_in_refund_type').id
                menu = self.env.ref('account.menu_action_move_in_refund_type').id
            else:
                action = self.env.ref('account.action_move_journal_line').id
                menu = self.env.ref('account.menu_action_move_journal_line_form').id
            # activity = self.env['mail.activity']
            self.env['mail.message'].sudo().create({
                'subject': 'Review asked',
                'message_type': "notification",
                'subtype_id': self.env.ref('mail.mt_note').id,
                'body': ("The user %s has clicked on ask review for"
                         " <a href='/web?debug=0#action=%s&id=%s&menu_id=%s&model=account.move&view_type=form'>%s</a>") % (
                        login_user.name, action, rec.id, menu, rec.name),
                'partner_ids': [(6, 0, needaction_partner_ids.ids)],
                'email_from': login_user.name,
                'record_name': rec.name,
                'author_id': login_user.partner_id.id,
                'notification_ids': h,
            })
            rec.write({
                'state': 'waiting'
            })





