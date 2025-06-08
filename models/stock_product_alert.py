# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockProduct(models.Model):
    _inherit = 'product.product'

    stock_threshold = fields.Float(string="Seuil de stock", default=1)
    diamter = fields.Char(string="Diametre")
    # type = fields.Char(string="Type")
    power = fields.Char(string="Puisssance(KW)")
    tension = fields.Char(string="Tension(V)")
    other_dim = fields.Char("Autres Dimensions")
    intensit = fields.Char(string="Intensité(A)")
    machine_id = fields.Many2one('res.partner', string="Machine", domain="[('is_company', '=', True)]")
    type_piece = fields.Char(string="Type de la Pièce")
    cat_piece = fields.Char(string="Categorie")
    position_id = fields.Many2one('stock.location', string="Position", domain="[('usage', '=', 'internal')]")
    usine_id = fields.Many2one('stock.warehouse',
                               string="Usine")


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
    type_piece = fields.Char(string="Type de la Pièce")
    cat_piece = fields.Char(string="Categorie")
    intensit = fields.Char(string="Intensité")
    power = fields.Char(string="Puisssance(KW)")
    other_dim = fields.Char("Autres Dimensions")
    tension = fields.Char(string="Tension")
    machine_id = fields.Many2one('res.partner', string="Machine", domain="[('is_company', '=', True)]" )
    position_id = fields.Many2one('stock.location', string="Position", domain="[('usage', '=', 'internal')]")
    usine_id = fields.Many2one('stock.warehouse',
                               string="Usine")

    is_below_threshold = fields.Boolean(string="Stock Insuffisant", compute="_compute_is_below_threshold", store=True)

    @api.depends('qty_available', 'stock_threshold')
    def _compute_is_below_threshold(self):
        for record in self:
            record.is_below_threshold = record.qty_available <= record.stock_threshold





class StockPicking(models.Model):
    _inherit = 'stock.picking'


    partner_id = fields.Many2one('res.partner', string="Machine", domain="[('is_company', '=', True)]", required=True)
    usine_id = fields.Many2one('stock.warehouse', string="Usine", required=True)
    user_id = fields.Many2one('res.users', string='Maganisier(e)', readonly=1, default=lambda self: self.env.user)
    tech_id = fields.Many2one('hr.employee', string="Technicien(e)")

    is_outgoing = fields.Boolean(
        compute='_compute_is_outgoing',
        help="True if the picking type is outgoing."
    )

    @api.depends('picking_type_id.code')
    def _compute_is_outgoing(self):
        for picking in self:
            picking.is_outgoing = picking.picking_type_id.code == 'outgoing'

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    partner_id = fields.Many2one(
        "res.partner",
        string="Machine",
        related="picking_id.partner_id",
        store=True
    )

    usine_id = fields.Many2one('stock.warehouse',
                               string="Usine",
                               related="picking_id.usine_id",
                               store=True)
    tech_id = fields.Many2one('hr.employee', string="Technicien(e)",
                              related="picking_id.tech_id",
                              store=True
                              )
    user_id = fields.Many2one('res.users', string='Maganisier(e)',
                              related="picking_id.user_id",
                              store=True
                              )


# class StockMov(models.Model):
#     _inherit = "stock.move"
#
#     tech_id = fields.Many2one('hr.employee', string="Technicien(e)",
#                               related="picking_id.tech_id",
#                               store=True
#                               )
#     user_id = fields.Many2one('res.users', string='Maganisier(e)',
#                               related="picking_id.user_id",
#                               store=True
#                               )
