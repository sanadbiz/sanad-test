const profile_selected_individual = document.querySelector('#profile_individual_img_id');
const profile_selected_brand = document.querySelector('#profile_brand_img_id');

const profile_selected_individual_check_icon = document.querySelector('#profile_individual_check_id');
const profile_selected_brand_check_icon = document.querySelector('#profile_brand_check_id');

const select_profile_setting = document.querySelector('#profile_selection_id');
if (profile_selected_individual) {
    profile_selected_individual.addEventListener('click', function () {
        profile_selected_individual_check_icon.style.display = 'block'
        profile_selected_brand_check_icon.style.display = 'none'
        select_profile_setting.value = 'individual'

    });

}

if (profile_selected_brand) {
    profile_selected_brand.addEventListener('click', function () {
        profile_selected_individual_check_icon.style.display = 'none'
        profile_selected_brand_check_icon.style.display = 'block'
        select_profile_setting.value = 'brand'
    });
}


//
//var selectedType = "";
//const VALID_TYPES = ['influencer', 'brand'];
//
//function submitChoice(element) {
//    const type = element.getAttribute("data-type");
//    if (VALID_TYPES.includes(type)) {
//        // Remove previous selection styling
//        document.querySelectorAll('.image-login').forEach(el => {
//            el.classList.remove('selected');
//            el.querySelector('.check-icon')?.classList.remove('visible');
//        });
//
//        // Add selection styling
//        selectedType = type;
//        element.classList.add('selected');
//        const checkIcon = element.querySelector('.check-icon');
//        if (checkIcon) {
//            checkIcon.classList.add('visible');
//        }
//    }
//}
//
//function confirmSelection() {
//    if (!selectedType) {
//        // Show error in more user-friendly way
//        const errorMsg = document.getElementById('selection-error');
//        if (errorMsg) {
//            errorMsg.style.display = 'block';
//        } else {
//            alert("الرجاء اختيار نوع الحساب");
//        }
//        return false;
//    }
//
//    // Redirect with selection
//    window.location.href = `/v1/profile_settings?type=${encodeURIComponent(selectedType)}`;
//    return true;
//}