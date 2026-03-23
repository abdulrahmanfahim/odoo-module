/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { useService } from "@web/core/utils/hooks";

patch(ReceiptScreen.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.notification = useService("notification");
    },

    async printReceipt() {
        const printAgentUrl = await this.orm.call(
            "ir.config_parameter",
            "get_param",
            ["direct_print.print_agent_url"]
        ) || "http://localhost:8080";

        const receiptEl = document.querySelector('.pos-receipt');
        if (printAgentUrl && receiptEl) {
            const receiptHtml = receiptEl.innerHTML;
            try {
                // 1. Send receipt content as HTML
                const printResponse = await fetch(`${printAgentUrl}/api/print/html`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content: receiptHtml }),
                });

                if (printResponse.ok) {
                    // 2. Feed and Cut
                    await fetch(`${printAgentUrl}/api/print/cut`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({}),
                    });

                    this.notification.add("Receipt sent to local printer", { type: "success" });
                    return;
                }
            } catch (error) {
                console.error("Direct print failed, falling back to browser", error);
            }
        }
        await super.printReceipt();
    }
});
