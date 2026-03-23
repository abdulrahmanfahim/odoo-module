from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    print_agent_url = fields.Char(
        string="Print Agent URL",
        config_parameter='direct_print.print_agent_url',
        default="http://localhost:8080"
    )
