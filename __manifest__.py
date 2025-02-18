# -*- coding: utf-8 -*-
{
    'name': "stock_okplast",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
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

