# -*- coding: utf-8 -*-
{
    'name': "exam_1",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized', 'Advanced_sale'
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', "sale"],

    # always loaded
    'data': [
        'security/group_advanced_sale.xml',
        'security/ir.model.access.csv',
        'views/res_partner_inherit_views.xml',
        'views/sales_orders_inherit_views.xml',
        'views/sales_orders_line_inherit_view.xml',
        'views/product_template_inherit_views.xml',
        'wizard/s_update_warranty_views.xml',
        'wizard/s_update_discount_code_views.xml',

    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
