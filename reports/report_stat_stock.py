# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
class StockMoveReport(models.AbstractModel):
    _name = 'report.stock_okplast.report_stat_stock'
    _description = 'Stock Move Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        wizard = self.env['wizard.print.report'].browse(docids)


        # Define base domain for stock moves
        domain = [
            ('date', '>=', wizard.date_start),
            ('date', '<=', wizard.date_end),
            ('picking_id.picking_type_id.code', '=', 'outgoing'),
            ('state', '=', 'done')
        ]

        # Apply filters based on filter_type
        if wizard.filter_type == 'partner' and wizard.machine_ids:
            domain.append(('picking_id.partner_id', 'in', wizard.machine_ids.ids))
        elif wizard.filter_type == 'warehouse' and wizard.usine_ids:
            domain.append(('picking_id.usine_id', 'in', wizard.usine_ids.ids))
        elif wizard.filter_type == 'product' and wizard.product_ids:
            domain.append(('product_id', 'in', wizard.product_ids.ids))
        elif wizard.filter_type == 'tech' and wizard.tech_ids:
            domain.append(('tech_id', 'in', wizard.tech_ids.ids))
        elif wizard.filter_type == 'user' and wizard.user_ids:
            domain.append(('user_id', 'in', wizard.user_ids.ids))

        moves = self.env['stock.move'].search(domain)

        report_data = {}

        for move in moves:
            if wizard.filter_type == 'partner':
                key = move.picking_id.partner_id
            elif wizard.filter_type == 'warehouse':
                key = move.picking_id.usine_id
            elif wizard.filter_type == 'product':
                key = move.product_id  # Grouping by product
            elif wizard.filter_type == 'tech':
                key = move.picking_id.tech_id  # Grouping by technicians
            elif wizard.filter_type == 'user':
                key = move.picking_id.user_id  # Grouping by Warehouse Person

            if key not in report_data:
                report_data[key] = {}

            product = move.product_id
            if product not in report_data[key]:
                report_data[key][product] = {'qty': 0, 'price': product.lst_price, 'total': 0}

            report_data[key][product]['qty'] += move.product_uom_qty
            report_data[key][product]['total'] = report_data[key][product]['qty'] * report_data[key][product]['price']

        return {'data': report_data,
                'date_start': wizard.date_start,  # Pass start date
                'date_end': wizard.date_end,  # Pass end date
                'filter_type': wizard.filter_type
                }