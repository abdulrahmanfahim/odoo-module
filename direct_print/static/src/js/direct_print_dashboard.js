/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class DirectPrintDashboard extends Component {
    setup() {
        // Dashboard setup logic
    }
}
DirectPrintDashboard.template = "direct_print.direct_print_dashboard";

registry.category("actions").add("direct_print_dashboard", DirectPrintDashboard);
