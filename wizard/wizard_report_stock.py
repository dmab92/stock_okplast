# -*- coding: utf-8 -*-
from odoo import models, fields, api
import io,base64
import xlsxwriter
from odoo.http import request


class WizardPrintReport(models.TransientModel):
    _name = "wizard.print.report"
    _description = "Wizard to Print Report"

    date_start = fields.Date(string="Date de Debut ", required=True, default=fields.Date.today)
    date_end = fields.Date(string="Date de Fin", required=True, default=fields.Date.today)
    machine_ids = fields.Many2many('res.partner', string='Machines')
    usine_ids = fields.Many2many('stock.warehouse', string='Warehouses')
    filter_type = fields.Selection([
        ('partner', 'Machine'),
        ('warehouse', 'Usine')
    ], string='Filter By', required=True, default='partner')

    report_type = fields.Selection([
        ('pdf', 'PDF'),
        ('excel', 'Excel')
    ], string='Report Type', required=True, default='pdf')


    def print_report(self):
        if self.report_type == 'pdf':
            return self.env.ref('stock_okplast.report_action_id').report_action(self)
        else:
            return self.export_xlsx_report()


    # def export_xlsx_report(self):
    #     output = io.BytesIO()
    #     workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    #     sheet = workbook.add_worksheet('Stock Moves')
    #
    #     # ✅ Récupération et insertion du logo
    #     company = self.env.company
    #     if company.logo:
    #         logo_data = base64.b64decode(company.logo)
    #         logo_io = io.BytesIO(logo_data)
    #         sheet.insert_image('A1', "logo.png", {'image_data': logo_io, 'x_scale': 0.5, 'y_scale': 0.5})
    #
    #     # ✅ Ajout du titre
    #     title = f"Rapport de stock du {self.date_start} au {self.date_end}"
    #     title_format = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14})
    #     sheet.merge_range('A3:E3', title, title_format)
    #
    #     # ✅ En-têtes du tableau
    #     headers = ['Entité', 'Produit', 'Quantité', 'Prix Unitaire', 'Total']
    #     header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
    #     for col, header in enumerate(headers):
    #         sheet.write(4, col, header, header_format)
    #
    #     # ✅ Définition du domaine de recherche
    #     domain = [('date', '>=', self.date_start), ('date', '<=', self.date_end), ('state', '=', 'done')]
    #
    #     if self.filter_type == 'partner' and self.machine_ids:
    #         domain.append(('picking_id.partner_id', 'in', self.machine_ids.ids))
    #     elif self.filter_type == 'warehouse' and self.usine_ids:
    #         domain.append(('picking_id.usine_id', 'in', self.usine_ids.ids))
    #
    #     moves = self.env['stock.move'].search(domain)
    #
    #     # ✅ Correction du tri
    #     if self.filter_type == 'partner':
    #         moves = moves.sorted(lambda m: m.picking_id.partner_id.name or "")
    #     elif self.filter_type == 'warehouse':
    #         moves = moves.sorted(lambda m: m.picking_id.usine_id.name or "")
    #
    #     row = 5  # Ligne de départ des données
    #
    #     for move in moves:
    #         group_name = move.picking_id.partner_id.name if self.filter_type == 'partner' else move.picking_id.usine_id.name or "Unknown"
    #         sheet.write(row, 0, group_name)
    #         sheet.write(row, 1, move.product_id.name)
    #         sheet.write(row, 2, move.product_uom_qty)
    #         sheet.write(row, 3, move.product_id.lst_price)
    #         sheet.write(row, 4, move.product_uom_qty * move.product_id.lst_price)
    #         row += 1
    #
    #     workbook.close()
    #     output.seek(0)
    #
    #     # ✅ Retourne une réponse HTTP correcte
    #     return request.make_response(
    #         output.getvalue(),
    #         headers=[
    #             ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
    #             ('Content-Disposition', 'attachment; filename=Stock_Report.xlsx')
    #         ]
    #     )

    def export_xlsx_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Stock Moves')

        # ✅ Ajout du titre
        title = f"Rapport de stock du {self.date_start} au {self.date_end}"
        title_format = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14})
        sheet.merge_range('A1:E1', title, title_format)

        # ✅ En-têtes du tableau
        #eaders = ['Entité', 'Produit', 'Quantité', 'Prix Unitaire', 'Total']
       #header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        # for col, header in enumerate(headers):
        #     sheet.write(4,col,header, header_format)

        # Define headers
        headers = ['Partner/Warehouse', 'Product', 'Quantity', 'Unit Price', 'Total']
        for col, header in enumerate(headers):
            sheet.write(0, col, header)

        # Define the domain for filtering stock moves
        domain = [
            ('date', '>=', self.date_start),
            ('date', '<=', self.date_end),
            ('picking_id.picking_type_id.code', '=', 'outgoing'),
            ('state', '=', 'done')
        ]

        if self.filter_type == 'partner' and self.machine_ids:
            domain.append(('picking_id.partner_id', 'in', self.machine_ids.ids))
        elif self.filter_type == 'warehouse' and self.usine_ids:
            domain.append(('picking_id.usine_id', 'in', self.usine_ids.ids))

        moves = self.env['stock.move'].search(domain)

        if self.filter_type == 'partner':
            moves = moves.sorted(lambda m: m.picking_id.partner_id.name or "")
        elif self.filter_type == 'warehouse':
            moves = moves.sorted(lambda m: m.picking_id.usine_id.name or "")

        row = 1

        for move in moves:
            # **Get the group name (Partner or Warehouse)**
            group_name = (
                move.picking_id.partner_id.name if self.filter_type == 'partner'
                else move.picking_id.usine_id.name if move.picking_id.usine_id else "Unknown"
            )

            # **Write the row data with the group name in the first column**
            product = move.product_id
            sheet.write(row, 0, group_name)  # Partner/Warehouse name
            sheet.write(row, 1, product.name)
            sheet.write(row, 2, move.product_uom_qty)
            sheet.write(row, 3, product.lst_price)
            sheet.write(row, 4, move.product_uom_qty * product.lst_price)
            row += 1

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


