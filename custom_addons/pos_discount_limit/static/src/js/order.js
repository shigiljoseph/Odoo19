/** @odoo-module **/
import { OrderDisplay } from "@point_of_sale/app/components/order_display/order_display";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";


patch(OrderDisplay.prototype, {
     setup() {
       super.setup();
       this.dialog = useService("dialog");
    },

     val_discount() {

        const order = this.props.order;
        const config = this.props.order.config;
        const maxLimit = config.limit * 100 || 0;
        const categoryIds = config.product_category_ids || [];

        const orderLines = order.lines || [];
        const selectedOrderLine = order.getSelectedOrderline();

        let totalPercent = 0;
        for (const l of orderLines) {
            console.log(l.product_id.name)

            const productCategIds = l.product_id.product_tmpl_id.pos_categ_ids.map(c => c.id) || [];
            const allowedCategIds = l.config.product_category_ids.map(c => c.id);
            const categMatch = productCategIds.some(id => allowedCategIds.includes(id));
            if (!categMatch ) continue;

            totalPercent += (l.discount || 0);
            console.log(l.discount)
            console.log(totalPercent)

            if (totalPercent > maxLimit) {

                selectedOrderLine.discount = 0;
                totalPercent -= l.discount
                this.dialog.add(AlertDialog, {
                    body: _t("Discount limit exceeds"),
                });
                break;

                return ;
            }
        }

        return ;
    },
});