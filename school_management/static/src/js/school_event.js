/** @odoo-module */
import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.schoolEventForm = publicWidget.Widget.extend({
    selector: 'form[action="/submit/event"]',
    events: {
        'change #start_date': '_onStartDateChange',
        'change #end_date': '_onEndDateChange',
    },

    _onStartDateChange: function (ev) {
        const startDate = new Date(ev.target.value);
        if (new Date().toISOString().split('T')[0] > startDate.toISOString().split('T')[0]) {
            alert("Invalid Date");
            ev.target.value = '';
        }
    },

    _onEndDateChange: function (ev) {
        const startDate = new Date(document.getElementById('start_date').value);
        const endDate = new Date(ev.target.value);
        if (endDate < startDate) {
            alert("End date must be after start date");
            ev.target.value = '';
        }
    }
});