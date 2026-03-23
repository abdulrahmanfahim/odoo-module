from odoo import models, fields, api
from odoo.exceptions import UserError
import requests
import json

class PosReceipt(models.Model):
    _name = 'pos.receipt'
    _description = 'Point of Sale Receipt'
    _order = "create_date desc"

    name = fields.Char(string='Receipt No.', required=True, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('pos.receipt.sequence'))
    content = fields.Text(string='Content', required=True, readonly=True)
    create_date = fields.Datetime(string='Date', readonly=True)

    @api.model
    def create_from_pos(self, receipt_html):
        return self.create({
            'content': receipt_html,
        })

    def action_print_receipt(self):
        self.ensure_one()
        agent_url = self.env['ir.config_parameter'].sudo().get_param('direct_print.agent_url')
        if not agent_url:
            raise UserError('Printer Agent URL is not configured in Direct Print settings.')

        if not agent_url.startswith(('http://', 'https://')):
            agent_url = 'http://' + agent_url

        print_url = f'{agent_url}/api/print/html'
        payload = {'content': self.content}
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(print_url, data=json.dumps(payload), headers=headers, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise UserError(f'Failed to connect to printer agent: {e}')

        return True
