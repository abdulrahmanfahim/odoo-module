from odoo import models, api, _
import requests
import base64
import logging

_logger = logging.getLogger(__name__)

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def direct_print(self, res_ids, agent_id=None):
        if not agent_id:
            # Fallback to default from settings if no specific agent is provided
            url = self.env['ir.config_parameter'].sudo().get_param('direct_print.print_agent_url', 'http://localhost:8080')
        else:
            agent = self.env['direct.print.agent'].browse(agent_id)
            url = agent.url

        for res_id in res_ids:
            # Generate PDF
            pdf_content, _ = self._render_qweb_pdf(res_id)
            
            # Encode to Base64
            encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')
            
            payload = {
                'content': encoded_pdf,
                'filename': f"{self.name}_{res_id}.pdf"
            }
            
            try:
                response = requests.post(f"{url}/api/print/pdf", json=payload, timeout=10)
                if response.status_code != 200:
                    _logger.error(f"Failed to print to agent at {url}: {response.text}")
            except Exception as e:
                _logger.error(f"Error connecting to print agent at {url}: {str(e)}")
        
        return True
