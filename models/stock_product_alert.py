# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockProduct(models.Model):
    _inherit = 'product.product'

    stock_threshold = fields.Float(string="Seuil de stock", default=1)
    diamter = fields.Char(string="Diametre")
    # type = fields.Char(string="Type")
    power = fields.Char(string="Puisssance(KW)")
    tension = fields.Char(string="Tension")
    other_dim = fields.Char("Autres Dimensions")
    intensit = fields.Char(string="Intensité")
    machine_id = fields.Many2one('res.partner', string="Machine")


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
    diamter = fields.Char(string="Diametre" )
    intensit = fields.Char(string="Intensité")
    power = fields.Char(string="Puisssance(KW)")
    other_dim = fields.Char("Autres Dimensions")
    tension = fields.Char(string="Tension")
    machine_id = fields.Many2one('res.partner', string="Machine")

    is_below_threshold = fields.Boolean(string="Stock Insuffisant", compute="_compute_is_below_threshold", store=True)

    @api.depends('qty_available', 'stock_threshold')
    def _compute_is_below_threshold(self):
        for record in self:
            record.is_below_threshold = record.qty_available <= record.stock_threshold




class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # partner_category_id = fields.Many2many(
    #     'res.partner.category',
    #     string="Usine",
    #     compute='_compute_partner_category',
    #     store=True
    # )
    partner_id = fields.Many2one('res.partner', string="Machine", required=True)
    usine_id = fields.Many2one('stock.warehouse', string="Usine")
    user_id = fields.Many2one('res.users', string='Opération Realisé par',   readonly=1, default=lambda self: self.env.user)

    # def _compute_usine(self):
    #     for record in self:
    #compute = '_compute_usine'
            #record.usine_id = record.partner_id.usine_id if record.partner_id.usine_id else False

# class ResPartner(models.Model):
#     _inherit = 'res.partner'
#
#     usine_id = fields.Many2one('stock.warehouse', string="Usine")
