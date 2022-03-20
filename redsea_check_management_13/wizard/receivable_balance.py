from odoo import models, fields, _,api
import xlsxwriter
from io import BytesIO
import base64
from datetime import datetime


class excelreport(models.TransientModel):
    _name = 'report.excel'

    excel_file = fields.Binary('Download report Excel', attachment=True, readonly=True)
    file_name = fields.Char('Excel File', size=64)



class TotalReceivableBalance(models.TransientModel):
    _name = 'receivable.balance'

    sales_person_id = fields.Many2one('res.users', string='Sales Person')
    partner_id = fields.Many2one('res.partner', string='Customer', domain=[('customer', '=', True)])
    report = fields.Binary(string='Download', readonly=True)
    report_name = fields.Char()
    excel_file = fields.Binary('Download', attachment=True, readonly=True)
    file_name = fields.Char('Excel File', size=64,readonly=1)

    def action_print(self):
        search_domain = []
        if self.sales_person_id:
            search_domain.append(('user_id', '=', self.sales_person_id.id))
        if self.partner_id:
            search_domain.append(('id', '=', self.partner_id.id))
        search_domain.append(('customer', '=', True))

        customers = self.env['res.partner'].search(search_domain)
        data = []
        for customer in customers:
            tot_post_pay = 0.0
            tot_refund_pay = 0.0
            tot_coll_pay = 0.0

            post_pays = self.env['account.payment'].search([
                ('partner_id', '=', customer.id),
                ('state', '=', 'posted'),
                ('payment_type', '=', 'inbound'),
                ('payment_method_code', '=', 'batch_payment')])
            for post_pay in post_pays:
                tot_post_pay += post_pay.amount

            refund_pays = self.env['account.payment'].search([
                ('partner_id', '=', customer.id),
                ('state', '=', 'refunded_under_collection'),
                ('payment_type', '=', 'inbound'),
                ('payment_method_code', '=', 'batch_payment')])
            for refund_pay in refund_pays:
                tot_refund_pay += refund_pay.amount

            under_coll_pays = self.env['account.payment'].search([
                ('partner_id', '=', customer.id),
                ('state', '=', 'under_coll'),
                ('payment_type', '=', 'inbound'),
                ('payment_method_code', '=', 'batch_payment')])
            for under_coll_pay in under_coll_pays:
                tot_coll_pay += under_coll_pay.amount

            data.append({
                'ref': customer.ref,
                'name': customer.name,
                'credit': customer.credit,
                'tot_post_pay': tot_post_pay,
                'tot_refund_pay': tot_refund_pay,
                'tot_post_refund': tot_post_pay + tot_refund_pay,
                'tot_coll_pay': tot_coll_pay,
                'tot_check_pay': tot_coll_pay + tot_post_pay + tot_refund_pay,
                'tot_all': tot_post_pay + tot_refund_pay + tot_coll_pay + customer.credit,
                'user_id': customer.user_id.name,
            })

        act = self.generate_excel(data)
        #
        # return {
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'report.excel',
        #     'res_id': act.id,
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'context': self.env.context,
        #     'target': 'new',
        # }
        return {
            'type': 'ir.actions.act_url',
            'name': 'Receivable Balance',
            'url': '/web/content/receivable.balance/%s/excel_file/receivable_balance.xlsx?download=true' % (
                self.id),
            'target': 'new'
        }


    def generate_excel(self, data):

        filename = 'Total Receivable Balance'

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Total Receivable Balance')

        without_borders = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'font_size': '12',

        })

        font_size_10 = workbook.add_format(
            {'font_name': 'KacstBook', 'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'border': 1})

        table_header_formate = workbook.add_format({
            'bold': 1,
            'border': 1,
            'bg_color': '#AAB7B8',
            'font_size': '12',
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True
        })

        sheet.set_column(0, 9, 15, without_borders)

        sheet.write('A1', 'كود العميل', table_header_formate)
        sheet.write('B1', 'اسم العميل', table_header_formate)
        sheet.write('C1', 'الرصيد الحالي', table_header_formate)
        sheet.write('D1', 'أوراق القبض', table_header_formate)
        sheet.write('E1', 'أوراق القبض المرتدة', table_header_formate)
        sheet.write('F1', 'اجمالي أوراق القبض بالخزينة', table_header_formate)
        sheet.write('G1', 'شيكات تحت التحصيل', table_header_formate)
        sheet.write('H1', 'اجمالي الشيكات', table_header_formate)
        sheet.write('I1', 'اجمالي المديونية', table_header_formate)
        sheet.write('J1', 'مهندس البيع', table_header_formate)

        row = 1
        col = 0

        for d in data:
            if d['tot_all'] != False:
                sheet.write(row, col, d['ref'] or '', font_size_10)
                sheet.write(row, col + 1, d['name'] or '', font_size_10)
                sheet.write(row, col + 2, d['credit'] or '', font_size_10)
                sheet.write(row, col + 3, d['tot_post_pay'] or '', font_size_10)
                sheet.write(row, col + 4, d['tot_refund_pay'] or '', font_size_10)
                sheet.write(row, col + 5, d['tot_post_refund'] or '', font_size_10)
                sheet.write(row, col + 6, d['tot_coll_pay'] or '', font_size_10)
                sheet.write(row, col + 7, d['tot_check_pay'] or '', font_size_10)
                sheet.write(row, col + 8, d['tot_all'] or '', font_size_10)
                sheet.write(row, col + 9, d['user_id'] or '', font_size_10)
                row += 1

        workbook.close()
        output.seek(0)

        self.write({'file_name': filename + str(datetime.today().strftime('%Y-%m-%d')) + '.xlsx'})
        self.excel_file = base64.b64encode(output.read())

        context = {
            'file_name': self.file_name,
            'excel_file': self.excel_file,
        }

        act_id = self.env['report.excel'].create(context)
        return act_id

        # self.report = base64.encodestring(output.read())
        # self.report_name = filename + str(datetime.today().strftime('%Y-%m-%d')) + '.xlsx'
