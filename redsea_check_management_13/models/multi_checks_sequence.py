# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class MultiChecksSequence(models.Model):
    _name = 'multi.checks.sequence'

    name = fields.Char()
    seq = fields.Integer()
    seq_year = fields.Integer()
