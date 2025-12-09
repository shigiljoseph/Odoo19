/** @odoo-module */
import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.StudentLeaveForm = publicWidget.Widget.extend({
    selector: '.school',
    events: {
        'change #student_id': '_onStudentChange',
        'change #half_day': '_onHalfDayChange',
        'change #start_date': '_onStartDateChange',
        'change #end_date': '_onEndDateChange'
    },

    _onStudentChange: function (ev) {
        const studentId = ev.target.value;
        console.log(studentId)
        if (!studentId) return;
        fetch(`/get_student_class/${studentId}`)
            .then(response => response.json())
            .then(data => {
                const option = document.getElementById('class_op');
                option.value = data.class_id;
                option.text = data.class_name;
                option.selected = true;
            });
    },

    _onHalfDayChange: function (ev) {
    console.log("innn")
        const DateDiv = document.querySelector('label[for="end_date"]').parentElement;
        if (ev.target.checked) {
            DateDiv.style.display = 'none';
        } else {
            DateDiv.style.display = 'block';
            document.getElementById('end_date').value = '';
        }
    },

    _onStartDateChange: function (ev) {
    console.log("innn")
    const startDate = new Date(ev.target.value);
    console.log(startDate)
        if (new Date().toISOString().split('T')[0] > startDate.toISOString().split('T')[0]) {
            alert('Past date can\'t be selected');
            ev.target.value = '';
        }
        if (document.getElementById('half_day').checked) {
            document.getElementById('end_date').value = ev.target.value;
        }
    },

    _onEndDateChange: function(ev){
    console.log("innn")
        const startDate = new Date(document.getElementById('start_date').value);
        const endDate = new Date(ev.target.value);
        if(endDate < startDate) {
            alert("End date cannot be before start date");
            ev.target.value = '';
        }

        if (startDate && endDate && startDate <= endDate) {
            let dayCount = 0;
            let currentDay = new Date(startDate);

            const halfDay = document.getElementById('half_day');

            console.log('hi')
            while (currentDay <= endDate) {
                const dayOfWeek = currentDay.getDay();
                if (dayOfWeek > 0 && dayOfWeek < 6) { // Monday to Friday (1-5)
                    dayCount++;
                }
                currentDay.setDate(currentDay.getDate() + 1);
            }

            document.getElementById('total_days').value = dayCount;

            if (halfDay && halfDay.checked) {
                document.getElementById('total_days').value = 0.5;
            }


        } else {
            document.getElementById('total_days').value = 0;
        }
    }
});   