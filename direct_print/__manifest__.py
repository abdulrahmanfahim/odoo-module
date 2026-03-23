{
    'name': 'Direct POS Printing Bridge',
    'version': '1.0.0',
    'category': 'Point of Sale',
    'summary': 'Bridge for direct printing to POS without browser/PDF dialogs',
    'description': """
        This module allows printing QWeb reports directly to a local Java print agent.
        Features:
        - HTTP/WebSocket bridge to Java print agent
        - Bypasses browser print dialogs
        - Configurable print agent endpoint
    """,
    'author': 'Abdu',
    'depends': ['base', 'web', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/pos_receipt_data.xml',
        'views/direct_print_agent_views.xml',
        'views/res_config_settings_views.xml',
        'views/direct_print_dashboard_actions.xml',
        'views/direct_print_menus.xml',
        'views/pos_receipt_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'direct_print/static/src/xml/direct_print_dashboard.xml',
            'direct_print/static/src/js/direct_print_dashboard.js',
        ],
        'point_of_sale.assets': [
            'direct_print/static/src/js/pos_direct_print.js',
            'direct_print/static/src/js/pos_save_receipt.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
