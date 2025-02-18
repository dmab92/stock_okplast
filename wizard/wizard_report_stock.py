# -*- coding: utf-8 -*-
from odoo import models, fields
import datetime

class WizardPrintReport(models.TransientModel):
    _name = "wizard.print.report"
    _description = "Wizard to Print Report"

    start_date = fields.Date(string="Date de Debut ", required=True, default=fields.Date.today)
    end_date = fields.Date(string="Date de Fin", required=True, default=fields.Date.today)
    machine_ids = fields.Many2many('res.partner')
    usine_ids = fields.Many2many('res.partner.category')
    type = fields.Selection([
        ('machine', 'Par Machine'),
        ('usine', 'Par Usine')
    ], string='Type de rapport')


    def print_report(self):
        return self.env.ref('stock_okplast.report_action_id').report_action(self)
