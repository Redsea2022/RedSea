# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class MakeApprovalWizard(models.TransientModel):
    _name = 'make.payment.approval.wizard'

    review = fields.Selection(string="Review", selection=[('approve', 'Approve'), ('reject', 'Reject')], required=True)
    reason = fields.Text(string='Reason')

    def make_approval(self):
        login = self.env.user
        invoice = self.env['account.payment'].browse(self.env.context.get('active_id'))
        for rec in self:
            if rec.review == 'approve':
                review = self.env['payment.approval.log'].sudo().create({
                    'user_id': login.id,
                    'date': fields.Datetime.now(),
                    'state': 'Approved',
                    'reason': rec.reason,
                })
                invoice.write({
                    'log_ids': [(4, review.id)],
                    'approval_cond': 'approved'
                })
            else:
                review = self.env['payment.approval.log'].sudo().create({
                    'user_id': login.id,
                    'date': fields.Datetime.now(),
                    'state': 'Rejected',
                    'reason': rec.reason,
                })
                invoice.write({
                    'log_ids': [(4, review.id)],
                    'approval_cond': 'rejected'
                })


class ApprovalLog(models.Model):
    _name = 'payment.approval.log'
    _description = 'Payment Approval Log'

    user_id = fields.Many2one(comodel_name="res.users", string="User")
    state = fields.Char(string="State")
    date = fields.Datetime(string="Date")
    reason = fields.Char(string="Reason")
    payment_id = fields.Many2one(comodel_name="account.payment")


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    approval_cond = fields.Selection([('draft', 'Draft'),
                                       ('waiting', 'Waiting Review'),
                                       ('approved', 'Approved'),
                                       ('rejected', 'Rejected'),
                                       ('post', 'POSTED')
                                       ], string='Approval Status', default='draft',copy=False)

    log_ids = fields.One2many(comodel_name="payment.approval.log", inverse_name="payment_id", readonly=1)

    def approval_reset(self):
        self.write({
            'approval_cond': 'draft'
        })

    def ask_review(self):
        for rec in self:
            needaction_partner_ids = self.env.ref('redsea_account_move_ask_review.audit_group').users.mapped(
                'partner_id')
            h = []
            o = self.env['mail.message'].search([('record_name', '!=', False), ('model', '=', 'account.payment')],
                                                limit=1)
            for g in needaction_partner_ids:
                h.append((0, 0, {'mail_message_id': o.id, 'res_partner_id': g.id}))
            login_user = self.env.user
            action = self.env.ref('account.action_account_payments_payable').id
            menu = self.env.ref('account.menu_action_account_payments_payable').id
            # activity = self.env['mail.activity']
            self.env['mail.message'].sudo().create({
                'subject': 'Payment Review asked',
                'message_type': "notification",
                'subtype_id': self.env.ref('mail.mt_note').id,
                'body': ("The user %s has clicked on ask review for"
                         " <a href='/web?debug=0#action=%s&id=%s&menu_id=%s&model=account.payment&view_type=form'>%s</a>") % (
                            login_user.name, action, rec.id, menu, rec.name),
                'partner_ids': [(6, 0, needaction_partner_ids.ids)],
                'email_from': login_user.name,
                'record_name': rec.name,
                'author_id': login_user.partner_id.id,
                'notification_ids': h,
            })
            rec.write({
                'approval_cond': 'waiting'
            })

    def post(self):
        res = super(AccountPayment, self).post()
        self.write({
            'approval_cond': 'post'
        })
        return res

    def action_draft(self):
        res = super(AccountPayment, self).action_draft()
        self.write({
            'approval_cond': 'draft'
        })
        return res
    # def post(self):
    #     """ Create the journal items for the payment and update the payment's state to 'posted'.
    #         A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
    #         and another in the destination reconcilable account (see _compute_destination_account_id).
    #         If invoice_ids is not empty, there will be one reconcilable move line per invoice to reconcile with.
    #         If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
    #     """
    #     AccountMove = self.env['account.move'].with_context(default_type='entry')
    #     for rec in self:
    #
    #         if rec.state != 'approved':
    #             raise UserError(_("Only an approved payment can be posted."))
    #
    #         if any(inv.state != 'posted' for inv in rec.invoice_ids):
    #             raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))
    #
    #         # keep the name in case of a payment reset to draft
    #         if not rec.name:
    #             # Use the right sequence to set the name
    #             if rec.payment_type == 'transfer':
    #                 sequence_code = 'account.payment.transfer'
    #             else:
    #                 if rec.partner_type == 'customer':
    #                     if rec.payment_type == 'inbound':
    #                         sequence_code = 'account.payment.customer.invoice'
    #                     if rec.payment_type == 'outbound':
    #                         sequence_code = 'account.payment.customer.refund'
    #                 if rec.partner_type == 'supplier':
    #                     if rec.payment_type == 'inbound':
    #                         sequence_code = 'account.payment.supplier.refund'
    #                     if rec.payment_type == 'outbound':
    #                         sequence_code = 'account.payment.supplier.invoice'
    #             rec.name = self.env['ir.sequence'].next_by_code(sequence_code, sequence_date=rec.payment_date)
    #             if not rec.name and rec.payment_type != 'transfer':
    #                 raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))
    #
    #         moves = AccountMove.create(rec._prepare_payment_moves())
    #         moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()
    #
    #         # Update the state / move before performing any reconciliation.
    #         move_name = self._get_move_name_transfer_separator().join(moves.mapped('name'))
    #         rec.write({'state': 'posted', 'move_name': move_name})
    #
    #         if rec.payment_type in ('inbound', 'outbound'):
    #             # ==== 'inbound' / 'outbound' ====
    #             if rec.invoice_ids:
    #                 (moves[0] + rec.invoice_ids).line_ids \
    #                     .filtered(lambda line: not line.reconciled and line.account_id == rec.destination_account_id)\
    #                     .reconcile()
    #         elif rec.payment_type == 'transfer':
    #             # ==== 'transfer' ====
    #             moves.mapped('line_ids')\
    #                 .filtered(lambda line: line.account_id == rec.company_id.transfer_account_id)\
    #                 .reconcile()
    #
    #     return True
