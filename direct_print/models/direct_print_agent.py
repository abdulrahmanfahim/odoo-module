from odoo import fields, models, api
import requests
import json

class DirectPrintAgent(models.Model):
    _name = 'direct.print.agent'
    _description = 'Direct Print Agent'

    name = fields.Char(string="Agent Name", required=True)
    ip_address = fields.Char(string="IP Address", required=True, default="127.0.0.1")
    port = fields.Char(string="Port", required=True, default="8080")
    active = fields.Boolean(default=True)
    
    @api.depends('ip_address', 'port')
    def _compute_url(self):
        for agent in self:
            agent.url = f"http://{agent.ip_address}:{agent.port}"

    url = fields.Char(compute="_compute_url", string="Agent URL")

    def test_connection(self):
        try:
            response = requests.get(f"{self.url}/api/print/status", timeout=5)
            if response.status_code == 200:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Success',
                        'message': f"Connected to {self.name}. {response.text}",
                        'sticky': False,
                        'type': 'success',
                    }
                }
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': f"Failed to connect: {str(e)}",
                    'sticky': True,
                    'type': 'danger',
                }
            }
