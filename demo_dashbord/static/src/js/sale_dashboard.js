/** @odoo-module */
import { registry } from '@web/core/registry';
import { useService } from "@web/core/utils/hooks";
const { Component, onMounted } = owl;
import { jsonrpc } from "@web/core/network/rpc_service";
import { _t } from "@web/core/l10n/translation";
import { useState } from "@odoo/owl";


export class SaleDashboard extends Component {
    setup() {
        this.action = useService("action");
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        onMounted(this.onMounted);
        this.state = useState({
            results:{},

        });
    }

    async onMounted() {
//        this.render_success_pack();
    }

//     async render_success_pack() {
//        const results = await this.orm.call('sale.order', 'get_sale_order_data',[[]]);
//        console.log("results.projects",results.projects)
//        this.state.results = results.vals;
//        this.state.companies = results.company_data;
//        }
}

SaleDashboard.template = "SaleDashboardTemplate";
registry.category("actions").add("sale_dashboard_tag", SaleDashboard);