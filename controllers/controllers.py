# -*- coding: utf-8 -*-
# from odoo import http


# class StockOkplast(http.Controller):
#     @http.route('/stock_okplast/stock_okplast', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_okplast/stock_okplast/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_okplast.listing', {
#             'root': '/stock_okplast/stock_okplast',
#             'objects': http.request.env['stock_okplast.stock_okplast'].search([]),
#         })

#     @http.route('/stock_okplast/stock_okplast/objects/<model("stock_okplast.stock_okplast"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_okplast.object', {
#             'object': obj
#         })

