# -*- coding: utf-8 -*-
import logging

import math

from odoo import models, fields, api, _, tools


class AccountMove(models.Model):
    _inherit = 'account.move'

    journey_num = fields.Char('رحلة رقم:')
    ship_name = fields.Char(' اسم الباخرة:')
    to_port = fields.Char('الى ميناء:')
    from_port = fields.Char('من ميناء:')
    msg_text = fields.Char('بيان الرسالة:')
    bill_of_lading = fields.Char('بوليصة رقم:')
    size_in_meter = fields.Char('الحجم بالمتر المكعب:')
    weight_in_ton = fields.Char('الوزن بالطن:')
    parcel_count = fields.Char('عدد الطرود:')
    is_journal_state_rel = fields.Selection(related='journal_id.journal_state')
    num_inv = fields.Char(string='Number', copy=False, readonly=True,)




    def print_report_invoice(self):
        for rec in self:
            if rec.is_journal_state_rel == 'unloading':
                return self.env.ref('redsea_invoices_print_out.daily_unloadings_report').report_action(self)
            if rec.is_journal_state_rel == 'freight':
                return self.env.ref('redsea_invoices_print_out.freight_report').report_action(self)
            if rec.is_journal_state_rel == 'outbound':
                return self.env.ref('redsea_invoices_print_out.outbound_ground_operations_report').report_action(self)
            if rec.is_journal_state_rel == 'shipping':
                return self.env.ref('redsea_invoices_print_out.shipping_returns_report').report_action(self)


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    journal_state = fields.Selection([('unloading', 'عوائد تفريغ'),
                                      ('shipping', 'عوائد شحن'),
                                      ('freight', 'نولون'),
                                      ('outbound', 'عمليات ارضية صادر')])


class ResCompany(models.Model):
    _inherit = 'res.company'

    address_st = fields.Text('Address 2')
    fax = fields.Char('Fax')


from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.move'


from odoo import models, fields, api, _, tools
import logging

_logger = logging.getLogger(__name__)

try:
    from num2words import num2words
except ImportError:
    _logger.warning("The num2words python library is not installed, amount-to-text features won't be fully available.")
    num2words = None


class ResCurrencyInherit(models.Model):
    _inherit = 'res.currency'

    def ar_amount_to_text(self, amount):
        self.ensure_one()

        def _num2words(number, lang):
            return num2words(number, lang=lang).title()

        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""

        formatted = "%.{0}f".format(self.decimal_places) % amount
        parts = formatted.partition('.')
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)

        lang_code = 'ar_SY'
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])
        amount_words = tools.ustr('{amt_value} {amt_word}').format(
            amt_value=num2words(integer_value, lang=lang.iso_code),
            amt_word='جنيها فقط لا غير' if self.is_zero(amount - integer_value) else 'جنيها',
        )
        if not self.is_zero(amount - integer_value):
            amount_words += ' ' + _('و') + tools.ustr(' {amt_value} {amt_word}').format(
                amt_value=num2words(fractional_value, lang=lang.iso_code),
                amt_word='قرشا فقط لا غير' if fractional_value > 10 else 'قروش فقط لا غير ',
            )
        return amount_words
