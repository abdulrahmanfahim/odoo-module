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
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/direct_print_agent_views.xml',
        'views/res_config_settings_views.xml',
        'views/direct_print_dashboard_actions.xml',
        'views/direct_print_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'direct_print/static/src/xml/direct_print_dashboard.xml',
            'direct_print/static/src/js/direct_print_dashboard.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
