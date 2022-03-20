# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RedSeaPaymentCancelDraftButtonsGroup(models.Model):
    _inherit = 'account.payment'

    def action_draft(self):
        res = super(RedSeaPaymentCancelDraftButtonsGroup, self).action_draft()
        self.message_post(body=self.env.user.name + " Is setting this record as a Draft!")
        return res

    def cancel(self):
        res = super(RedSeaPaymentCancelDraftButtonsGroup, self).cancel()
        self.message_post(body=self.env.user.name + " Has Canceled This record")
        return res


class RedSeaInvoiceCancelDraftButtonsGroup(models.Model):
    _inherit = 'account.move'

    def button_draft(self):
        res = super(RedSeaInvoiceCancelDraftButtonsGroup, self).button_draft()
        if self:
            self.message_post(body=self.env.user.name + " Is setting this record as a Draft!")
        return res

    def button_cancel(self):
        res = super(RedSeaInvoiceCancelDraftButtonsGroup, self).button_cancel()
        self.message_post(body=self.env.user.name + " Has Canceled This record")
        return res
