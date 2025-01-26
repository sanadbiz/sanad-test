/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.PasswordResetValidation = publicWidget.Widget.extend({
    selector: 'form[action="/web/reset_password"]',
    events: {
        'submit': '_onFormSubmit'
    },

    start() {
        this.$submitButton = this.$el.find('.login-button');
    },

    _onFormSubmit(ev) {
        if (this.$submitButton.prop('disabled')) {
            ev.preventDefault();
            return;
        }

        this.$submitButton.prop('disabled', true);

        setTimeout(() => {
            this.$submitButton.prop('disabled', false);
            this.$submitButton.removeClass('button-processing');
        }, 10000);
    }
});