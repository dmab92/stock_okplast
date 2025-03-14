# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
class StockMoveReport(models.AbstractModel):
    _name = 'report.stock_okplast.report_stat_stock'
    _description = 'Stock Move Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        wizard = self.env['wizard.print.report'].browse(docids)
        domain = [
            ('date', '>=', wizard.date_start),
            ('date', '<=', wizard.date_end),
            ('picking_id.picking_type_id.code', '=', 'outgoing'),
            ('state', '=', 'done')
        ]
        if wizard.filter_type == 'partner' and wizard.machine_ids:
            domain.append(('picking_id.partner_id', 'in', wizard.machine_ids.ids))
        elif wizard.filter_type == 'warehouse' and wizard.usine_ids:
            domain.append(('picking_id.usine_id', 'in', wizard.usine_ids.ids))

        moves = self.env['stock.move'].search(domain)

        report_data = {}
        for move in moves:
            key = move.picking_id.partner_id if wizard.filter_type == 'partner' else move.picking_id.usine_id
            if key not in report_data:
                report_data[key] = {}
            product = move.product_id
            if product not in report_data[key]:
                report_data[key][product] = {'qty': 0, 'price': product.lst_price, 'total': 0}
            report_data[key][product]['qty'] += move.product_uom_qty
            report_data[key][product]['total'] = report_data[key][product]['qty'] * report_data[key][product]['price']

        return {'data': report_data}

        # return {
        #     'doc_ids': docids,
        #     'doc_model': 'stock.move',
        #     'o': docs[0],  # Pass the main document object
        #     'data': report_data,  # Pass the data dictionary
        #     '
        # }