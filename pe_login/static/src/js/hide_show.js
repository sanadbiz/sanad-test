$(document).ready(function() {
    $(".toggle-password").click(function() {
        $(this).toggleClass("fa-eye-slash fa-eye");
        var input = $(this).closest('.password-field-container').find('input[type="password"], input[type="text"]');
        input.attr("type", input.attr("type") === "password" ? "text" : "password");
    });
});