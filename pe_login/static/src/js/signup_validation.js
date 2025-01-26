/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.PasswordValidation = publicWidget.Widget.extend({
    selector: '.password-validation-input',
    events: {
        'input': '_onPasswordInput',
        'focus': '_onPasswordFocus',
        'blur': '_onPasswordBlur',
        'submit': '_onFormSubmit',
    },

    start() {
        this.$passwordFields = this.$el.find('div.password-field-container input[type="password"]');
        this.$submitButton = $('.login-button');
        this.password = $('input[name="password"]');
        this.confirm_password = $('input[name="confirm_password"]')

        this.$passwordFields.each((index, field) => {
            this.createValidationContainer($(field));
        });

    },

    createValidationContainer($passwordField) {
        // Create unique validation feedback container for each field
        const $validationContainer = $('<div>', {
            'class': 'password-validation-container',
            'style': 'color: #666; margin-top: 5px;'
        });

        $passwordField.after($validationContainer);
    },

    _onPasswordInput(ev) {
        const $currentField = $(ev.target);
        const password = ev.target.value;

        const isValid = this.validatePassword($currentField, password);

         if (this.confirm_password.length) {
            this.validatePasswordMatch();
        }
        this.updateSubmitButton();
    },



    _onPasswordFocus(ev) {
        const $currentField = $(ev.target);
        const password = ev.target.value;

        this.validatePassword($currentField, password);
        $currentField.next('.password-validation-container').show();
    },

    _onPasswordBlur(ev) {
        const $currentField = $(ev.target);
        $currentField.next('.password-validation-container').hide();
    },

    validatePassword($passwordField, password) {
        // Validation rules
        const validations = [
            {
                test: (pw) => pw.length >= 8,
                message: 'يجب أن تكون كلمة المرور 8 أحرف على الأقل',
                icon: '✖️'
            },
            {
                test: (pw) => /[A-Z]/.test(pw),
                message: 'يجب أن تحتوي على حرف كبير واحد على الأقل',
                icon: '✖️'
            },
            {
                test: (pw) => /[a-z]/.test(pw),
                message: 'يجب أن تحتوي على حرف صغير واحد على الأقل',
                icon: '✖️'
            },
            {
                test: (pw) => /[0-9]/.test(pw),
                message: 'يجب أن تحتوي على رقم واحد على الأقل',
                icon: '✖️'
            },
            {
                test: (pw) => /[!@#$%^&*(),.?":{}|<>]/.test(pw),
                message: 'يجب أن تحتوي على حرف خاص واحد على الأقل',
                icon: '✖️'
            }
        ];

        // Generate validation feedback
        const feedback = validations.map(validation => {
            const isPassed = validation.test(password);
            return {
                message: validation.message,
                icon: isPassed ? '✔️' : '✖️',
                status: isPassed ? 'valid' : 'invalid'
            };
        });

        // Render validation feedback for this specific field
        this.renderValidationFeedback($passwordField, feedback);

        // Return whether all validations passed
        return feedback.every(item => item.status === 'valid');
    },

    renderValidationFeedback($passwordField, feedback) {
        // Find or create validation container for this specific field
        let $validationContainer = $passwordField.next('.password-validation-container');

        // Clear previous feedback
        $validationContainer.empty();

        // Render new feedback
        feedback.forEach(item => {
            const $validationItem = $('<div>', {
                'class': `validation-item ${item.status}`,
                'style': `
                    color: ${item.status === 'valid' ? 'green' : 'red'};
                    font-size: 0.8em;
                `
            }).html(`${item.icon} ${item.message}`);

            $validationContainer.append($validationItem);
        });
    },

    validatePasswordMatch() {
        const password = this.password.val();
        const confirmPassword = this.confirm_password.val();
        const $validationContainer = this.confirm_password.next('.password-validation-container');

        // Clear previous feedback
        $validationContainer.empty();

        if (password !== confirmPassword) {
            // Add password match validation feedback
            const $validationItem = $('<div>', {
                'class': 'validation-item invalid',
                'style': 'color: red; font-size: 0.8em;'
            }).html('✖️ كلمة المرور غير متطابقة');

            $validationContainer.append($validationItem);
            return false;
        } else if (confirmPassword) {
            // Add match confirmation if confirm password is not empty
            const $validationItem = $('<div>', {
                'class': 'validation-item valid',
                'style': 'color: green; font-size: 0.8em;'
            }).html('✔️ كلمة المرور متطابقة');

            $validationContainer.append($validationItem);
            return true;
        }

        return false;
    },

    updateSubmitButton() {
        const allPasswordsValid = this.$passwordFields.toArray().every(field => {
            const password = $(field).val();
            return this.validatePassword($(field), password);
        });
        const passwordsMatch = this.validatePasswordMatch();
        this.$submitButton.prop('disabled', !(allPasswordsValid && passwordsMatch));
    },

    _onFormSubmit(ev) {
    if (this.$submitButton.prop('disabled')) {
        ev.preventDefault();
        return;
    }
    this.$submitButton.prop('disabled', true);
    setTimeout(() => {
        this.$submitButton.prop('disabled', false);
    }, 10000);
},

});