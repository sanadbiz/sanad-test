document.addEventListener('DOMContentLoaded', function() {
    const otpInputs = document.querySelectorAll('.code_number');

    otpInputs.forEach((input, index) => {
        input.addEventListener('input', function() {
            // Limit to single digit
            this.value = this.value.slice(0, 1);

            // Move to next input if a digit is entered
            if (this.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', function(e) {
            // Move to previous input on backspace when empty
            if (e.key === 'Backspace' && this.value === '' && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
    });

    // First input paste event
    otpInputs[0].addEventListener('paste', function(e) {
        e.preventDefault();
        const pastedData = e.clipboardData.getData('text');
        const pastedDigits = pastedData.replace(/\D/g, '').slice(0, otpInputs.length);

        pastedDigits.split('').forEach((digit, i) => {
            if (i < otpInputs.length) {
                otpInputs[i].value = digit;
                if (i < otpInputs.length - 1) {
                    otpInputs[i + 1].focus();
                }
            }
        });
    });
});