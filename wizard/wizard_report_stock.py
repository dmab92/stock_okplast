# -*- coding: utf-8 -*-
from odoo import models, fields, api
import io,base64
import xlsxwriter
from odoo.exceptions import ValidationError


class WizardPrintReport(models.TransientModel):
    _name = "wizard.print.report"
    _description = "Wizard to Print Report"

    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)
    machine_ids = fields.Many2many('res.partner', string='Machines')
    usine_ids = fields.Many2many('stock.warehouse', string='Warehouses')
    product_ids = fields.Many2many('product.product', string='Products')
    filter_type = fields.Selection([
        ('partner', 'Machine'),
        ('warehouse', 'Usine'),
        ('product', 'Product')
    ], string='Filter By', required=True, default='partner')

    report_type = fields.Selection([
        ('pdf', 'PDF'),
        ('excel', 'Excel')
    ], string='Report Type', required=True, default='pdf')

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end:
                if record.date_start > record.date_end:
                    raise ValidationError("The start date cannot be later than the end date.")


    def print_report(self):
        if self.report_type == 'pdf':
            return self.env.ref('stock_okplast.report_action_id').report_action(self)
        else:
            return self.export_xlsx_report()

    def export_xlsx_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Stock Moves')
        filter_type_value = dict(self._fields['filter_type'].selection).get(self.filter_type)

        # Merge range and set bold formatting for the report header
        sheet.merge_range('B1:K1',
                          "RAPPORT D'UTILISATION DES PIECES PAR " + filter_type_value.upper() +
                          " LA PERIODE DU " + self.date_start.strftime('%d/%m/%Y') +
                          " AU " + self.date_end.strftime('%d/%m/%Y'),
                          workbook.add_format({'bold': True}))

        # Headers for the table
        headers = ['Partner/Warehouse/Product', 'Product', 'Quantity', 'Unit Price', 'Total']
        for col, header in enumerate(headers):
            sheet.write(2, col, header, workbook.add_format({'bold': True}))

        # Define the domain for filtering stock moves
        domain = [
            ('date', '>=', self.date_start),
            ('date', '<=', self.date_end),
            ('picking_id.picking_type_id.code', '=', 'outgoing'),
            ('state', '=', 'done')
        ]

        # Adjust domain for each filter type
        if self.filter_type == 'partner' and self.machine_ids:
            domain.append(('picking_id.partner_id', 'in', self.machine_ids.ids))
        elif self.filter_type == 'warehouse' and self.usine_ids:
            domain.append(('picking_id.usine_id', 'in', self.usine_ids.ids))
        elif self.filter_type == 'product' and self.product_ids:
            domain.append(('product_id', 'in', self.product_ids.ids))

        # Get stock moves based on the domain
        moves = self.env['stock.move'].search(domain)

        # Sort based on the selected filter type
        if self.filter_type == 'partner':
            moves = moves.sorted(lambda m: m.picking_id.partner_id.name or "")
        elif self.filter_type == 'warehouse':
            moves = moves.sorted(lambda m: m.picking_id.usine_id.name or "")
        elif self.filter_type == 'product':
            moves = moves.sorted(lambda m: m.product_id.name or "")

        row = 4
        total_sum = 0

        # Write the data in rows
        for move in moves:
            # **Get the group name (Partner/Warehouse/Product)**
            group_name = (
                move.picking_id.partner_id.name
                if self.filter_type == 'partner'
                else move.picking_id.usine_id.name
                if move.picking_id.usine_id
                else move.product_id.name
                if self.filter_type == 'product'
                else "Unknown"
            )

            # **Write the row data with the group name in the first column**
            product = move.product_id
            total = move.product_uom_qty * product.lst_price
            sheet.write(row, 0, group_name)  # Partner/Warehouse/Product name
            sheet.write(row, 1, product.name)
            sheet.write(row, 2, move.product_uom_qty)
            sheet.write(row, 3, product.lst_price)
            sheet.write(row, 4, total)
            total_sum += total
            row += 1
            # Write the general total at the end of the report
        sheet.write(row, 3, "Total", workbook.add_format({'bold': True}))  # "Total" in the Unit Price column
        sheet.write(row, 4, total_sum, workbook.add_format(
            {'bold': True, 'num_format': '#,##0'}))  # The total sum in the "Total" column

        workbook.close()
        output.seek(0)

        file_data = base64.b64encode(output.getvalue()).decode()

        attachment = self.env['ir.attachment'].create({
            'name': 'Stock_Move_Report.xlsx',
            'type': 'binary',
            'datas': file_data,
            'res_model': 'stock.move.report.wizard',
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }

    # def export_xlsx_report(self):
    #     output = io.BytesIO()
    #     workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    #     sheet = workbook.add_worksheet('Stock Moves')
    #     filter_type_value = dict(self._fields['filter_type'].selection).get(self.filter_type)
    #
    #
    #     sheet.merge_range('C1:K1',
    #                       "RAPPORT D'UTILISATION DES PIECES PAR " + filter_type_value.upper() +
    #                       " LA PERIODE DU " + self.date_start.strftime('%d/%m/%Y') +
    #                       " AU " + self.date_end.strftime('%d/%m/%Y'),
    #                       workbook.add_format({'bold': True}))
    #
    #     headers = ['Partner', 'Product', 'Quantity', 'Unit Price', 'Total']
    #     for col, header in enumerate(headers):
    #         sheet.write(2, col, header,workbook.add_format({'bold': True}))
    #
    #     # Define the domain for filtering stock moves
    #     domain = [
    #         ('date', '>=', self.date_start),
    #         ('date', '<=', self.date_end),
    #         ('picking_id.picking_type_id.code', '=', 'outgoing'),
    #         ('state', '=', 'done')
    #     ]
    #
    #     if self.filter_type == 'partner' and self.machine_ids:
    #         domain.append(('picking_id.partner_id', 'in', self.machine_ids.ids))
    #     elif self.filter_type == 'warehouse' and self.usine_ids:
    #         domain.append(('picking_id.usine_id', 'in', self.usine_ids.ids))
    #
    #     moves = self.env['stock.move'].search(domain)
    #
    #     if self.filter_type == 'partner':
    #         moves = moves.sorted(lambda m: m.picking_id.partner_id.name or "")
    #     elif self.filter_type == 'warehouse':
    #         moves = moves.sorted(lambda m: m.picking_id.usine_id.name or "")
    #
    #
    #     row = 4
    #
    #     for move in moves:
    #         # **Get the group name (Partner or Warehouse)**
    #         group_name = (
    #             move.picking_id.partner_id.name
    #             if self.filter_type == 'partner'
    #             else move.picking_id.usine_id.name
    #
    #             if move.picking_id.usine_id
    #             else "Unknown"
    #         )
    #
    #         # **Write the row data with the group name in the first column**
    #         product = move.product_id
    #         sheet.write(row, 0, group_name)  # Partner/Warehouse name
    #         sheet.write(row, 1, product.name)
    #         sheet.write(row, 2, move.product_uom_qty)
    #         sheet.write(row, 3, product.lst_price)
    #         sheet.write(row, 4, move.product_uom_qty * product.lst_price)
    #         row += 1
    #
    #     workbook.close()
    #     output.seek(0)
    #
    #     file_data = base64.b64encode(output.getvalue()).decode()
    #
    #     attachment = self.env['ir.attachment'].create({
    #         'name': 'Stock_Move_Report.xlsx',
    #         'type': 'binary',
    #         'datas': file_data,
    #         'res_model': 'stock.move.report.wizard',
    #         'res_id': self.id,
    #         'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    #     })
    #
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': '/web/content/%s?download=true' % attachment.id,
    #         'target': 'self',
    #     }


