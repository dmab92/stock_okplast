# -*- coding: utf-8 -*-
{
    'name': "stock_okplast",

    'summary': "Simplifier le processus d’inventaire, de garantir une "
               "meilleure organisation des pièces, et de fournir un outil permettant un suivi précis des"
               "opérations liées à l'entrée, la sortie et la consommation des pièces de machines",

    'description': """
Organisation et Gestion des Pièces
 Toutes les pièces de machines doivent être codifiées et enregistrées dans la plateforme
numérique par les employés.
 Les étagères de stockage sont actuellement numérotées de A1 à A6, avec 50 colonnes
d’étagères recensées (et d'autres pourraient être ajoutées).
 La solution doit permettre un inventaire par rangée avec export en format PDF et
Excel.
Suivi des Opérations (Entrée/Sortie)
 Les entrées et les sorties de pièces doivent être enregistrées avec :
o Date et heure automatiques.
o Nom du personnel ayant effectué l’opération.
 Aucune suppression de matériel ne doit être possible par les employés non habilités.
Prévention et Gestion des Stocks
 Le système doit prévenir les ruptures de stock des pièces à partir d’un seuil défini
préalablement défini. 
Lors de l’utilisation des filtres, l’outil doit proposer une pièce proche en cas de rupture
du stock exact.
Fonctionnalités Avancées
 Génération de rapports d’inventaire sur un intervalle de temps(date de debut et date de
fin) à la demande
 Description précise des articles (nom, diamètre, etc.).
 Pertinence des filtres (par code, par diamètre, par catégorie, etc.).
 Ajout des informations suivantes :
o Prix des pièces.
o Montant de la consommation des pièces par machine et par usine.
o Nombre de pièces consommées par machine et par usine.
 Filtrage financier : prix total de pièces consommés par machine et par usine sur un
intervalle de temps.
Integration et Infrastructure
 Le serveur doit être connecté au réseau existant (point à point) pour rendre les
machines opérationnelles
    """,

    'author': "MT CONSULTING SARL",
    'website': "https://www.mtconsultingsarl.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'views/stock_product_alert.xml',
        #'security/ir.model.access.csv',
        'wizard/wizard_report_stock.xml',
        'reports/report_stat_stock.xml',
        'menu_okplast.xml'
    ],

     'license': 'LGPL-3',
     'application': True,
    'installable': True,
    'auto_install': False,
}

