/** @odoo-module */

import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.StudentRegistrationForm = publicWidget.Widget.extend({
    selector : '.student',
    events : {
        'change #dob' : '_onDobChange',
        'click #new_button': '_onNewButtonClick',
    },

    _onDobChange : function(student){
        const birthDate = new Date(student.target.value);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();

        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        document.getElementById('age').value = age
    },

    _onNewButtonClick : function(Bn){
        Bn.preventDefault();
        window.location = `/student_registration`;
    },


});