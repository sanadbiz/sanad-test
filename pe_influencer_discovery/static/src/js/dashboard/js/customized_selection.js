$(document).ready(function () {
    $(document).on("click", ".custom-select__trigger", function (e) {
        e.stopPropagation();
        const $customSelect = $(this).closest(".custom-select");
        $customSelect.toggleClass("open");
    });

    $(document).on("click", function (e) {
        const $target = $(e.target);
        const $customSelect = $(".custom-select");

        if (!$target.closest(".custom-select").length) {
            $customSelect.removeClass("open");
        }
    });

    $(document).on("click", ".custom-select__option", function () {
        const $selectedOption = $(this);
        const $customSelect = $selectedOption.closest(".custom-select");
        const $selectTrigger = $customSelect.find(".custom-select__trigger");
        const $options = $customSelect.find(".custom-select__option");

        $options.removeClass("selected").find(".tick-icon").addClass("hidden");
        $selectedOption.addClass("selected").find(".tick-icon").removeClass("hidden");

        const $optionTextIcon = $selectedOption.find(".option-text-icon").clone();
        const $optionText = $selectedOption.find(".option-text").clone();

        if ($optionTextIcon.length) {
            $selectTrigger.find("span").html($optionTextIcon);
        } else {
            $selectTrigger.find("span").html($optionText);
        }

        $customSelect.removeClass("open");
    });

    $(".custom-select").each(function () {
        const $customSelect = $(this);
        const $selectTrigger = $customSelect.find(".custom-select__trigger span");
        const $firstOption = $customSelect.find(".custom-select__option").first();

        $firstOption.addClass("selected").find(".tick-icon").removeClass("hidden");

        const $optionTextIcon = $firstOption.find(".option-text-icon").clone();
        const $optionText = $firstOption.find(".option-text").clone();

        if ($optionTextIcon.length) {
            $selectTrigger.html($optionTextIcon);
        } else {
            $selectTrigger.html($optionText);
        }
    });
});