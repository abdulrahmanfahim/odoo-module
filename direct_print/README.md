# Direct POS Printing Bridge (Odoo)

This module allows Odoo to print reports directly to a local Java print agent, bypassing the browser's print dialog.

## Features
- Direct printing from server-side to local IP
- Multi-agent management (per POS terminal)
- Global fallback configuration
- Automatic PDF rendering and transmission

## Configuration
1. Install the module.
2. Go to `Direct Print > Configuration > Settings` to set the global print agent URL.
3. Go to `Direct Print > Agents` to add specific POS terminals (IP/Port).

## Usage
Reports can be printed programmatically via the `direct_print` method on `ir.actions.report`.
Example:
```python
report = self.env.ref('account.account_invoices')
report.direct_print(invoice_ids, agent_id=my_agent.id)
```
