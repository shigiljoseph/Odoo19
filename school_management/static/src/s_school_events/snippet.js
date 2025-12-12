/** @odoo-module */
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";

function chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}

publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
    selector: '.s_school_event_snippet',
    async willStart() {
        const result = await rpc('/get_event_details', {});
        if (result) {
            this.events = result.events;
        }
    },
    start() {
        if (this.events && this.events.length > 0) {
            const chunks = chunk(this.events, 3);
            console.log(chunks)
            const id = 'carousel_' + Math.random().toString(36).substr(2, 9);
            chunks[0].is_active = true;
            this.$target.empty().html(renderToElement('school_management.school_event_snippet', { result: { events: chunks , id :id} }));
        } else {
            this.$target.empty().html('<p>No events found.</p>');
        }
    }
});   