/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { useService } from "@web/core/utils/hooks";
import { onMounted } from "@odoo/owl";

patch(ReceiptScreen.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.notification = useService("notification");

        onMounted(() => {
            // Automatically trigger print when the receipt screen is displayed
            this.printReceipt();
        });
    },

    async printReceipt() {
        const printAgentUrl = await this.orm.call(
            "ir.config_parameter",
            "get_param",
            ["direct_print.print_agent_url"]
        ) || null;

        if (!printAgentUrl) {
            // If no agent is configured, fall back to the default browser printing.
            // This ensures normal Odoo behavior is preserved if the agent isn't set up.
            await super.printReceipt();
            return;
        }

        const receiptEl = this.el.querySelector('.pos-receipt');
        if (receiptEl) {
            const receiptHtml = receiptEl.innerHTML;
            try {
                // 1. Send receipt content as HTML
                const printResponse = await fetch(`${printAgentUrl}/api/print/html`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content: receiptHtml }),
                });

                if (!printResponse.ok) {
                    const errorBody = await printResponse.text();
                    throw new Error(`Print agent returned status ${printResponse.status}: ${errorBody}`);
                }
                
                // 2. Feed and Cut
                const cutResponse = await fetch(`${printAgentUrl}/api/print/cut`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({}),
                });

                if (!cutResponse.ok) {
                    const errorBody = await cutResponse.text();
                    throw new Error(`Print agent cut command failed with status ${cutResponse.status}: ${errorBody}`);
                }

                this.notification.add("Receipt sent to local printer.", { type: "success" });

            } catch (error) {
                console.error("Direct print failed:", error);
                this.notification.add("Direct print failed. Check agent and printer.", { type: "danger", sticky: true });
                // IMPORTANT: Do not fall back to super.printReceipt() here.
                // This fulfills the requirement to override browser printing entirely.
            }
        } else {
            this.notification.add("Could not find receipt content to print.", { type: "warning" });
        }
    }
});
