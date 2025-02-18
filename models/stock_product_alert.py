# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockProduct(models.Model):
    _inherit = 'product.product'

    stock_threshold = fields.Float(string="Seuil de stock", default=1)



    @api.model
    def get_low_stock_products(self):
        return self.env['product.product'].search([('qty_available', '<=', 'stock_threshold')])


class ProductTemplate(models.Model):
    _inherit = 'product.template'  # Si tu veux appliquer cela à tous les produits

    stock_threshold = fields.Float(
        string="Seuil de Stock",
        default=1,
        help="Le seuil à ne pas dépasser pour déclencher un avertissement de stock faible."
    )

    is_below_threshold = fields.Boolean(string="Stock Insuffisant", compute="_compute_is_below_threshold", store=True)

    @api.depends('qty_available', 'stock_threshold')
    def _compute_is_below_threshold(self):
        for record in self:
            record.is_below_threshold = record.qty_available <= record.stock_threshold