from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    agent_url = fields.Char(
        string="Print Agent URL",
        config_parameter='direct_print.agent_url',
        help="The URL of the Direct Print Agent (e.g. http://localhost:8080)"
    )
