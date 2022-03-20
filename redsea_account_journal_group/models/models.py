# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class redsea_account_journal_group(models.Model):
#     _name = 'redsea_account_journal_group.redsea_account_journal_group'
#     _description = 'redsea_account_journal_group.redsea_account_journal_group'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
