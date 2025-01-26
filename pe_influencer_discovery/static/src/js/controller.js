// on_code verification submission

const on_code_submit_form = document.querySelector('#code_verification_submit_btn_id');
const form = document.getElementById('code_verification_form');
if (form) {
    form.onsubmit = function (event) {
        event.preventDefault();

        let code_structure = []
        let code_length = 6
        for (let i = 1; i <= code_length; i++) {
            let val = document.getElementById(`code_${i}`).value
            if (!val.length) {
                document.getElementById('wrong_code').style.display = 'block';
                break;
            } else {
                code_structure.push(+val)
            }
        }
        if (code_structure.length == 6) {
            let email = document.getElementById('session_email_id').value
            let url = '/web/create_password'
            let data = {"code_structure": code_structure, "email": email}
            submit_to_server(url, data);
        }
    };
}
const form_profile_setting = document.getElementById('profile_settings_form_id');
if (form_profile_setting) {
    form_profile_setting.onsubmit = function (event) {
        event.preventDefault();
        let selection = document.getElementById('profile_selection_id');
        let url = '/web/profile_settings_data_filled'
        let data = {"profile_setting_value": selection.value}
        submit_to_server(url, data)
    };
}

const form_brand_info = document.getElementById('profile_brand_info_form_id');
if (form_brand_info) {
    form_brand_info.onsubmit = function (event) {
        event.preventDefault();
        let first_name = document.getElementById('b_first_name');
        let last_name = document.getElementById('b_last_name');
        let brand_name = document.getElementById('b_brand_name');
        let mobile_number = document.getElementById('b_mobile_number');
        let url = '/web/brand_info'
        let data = {
                "first_name": first_name.value,
                "last_name": last_name.value,
                "brand_name": brand_name.value,
                "mobile_number": mobile_number.value,
            }
        submit_brand_info(url, data)
    };
}


async function submit_to_server(url, data) {

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        const responseData = await response.json();
        if (responseData.reroute_location) {
            window.location.href = responseData.reroute_location;
        }
        else if(responseData.error === "invalid_code")
        {
            document.getElementById('wrong_code').style.display = 'block';
        }

    } catch (error) {
        console.error('Error:', error);
    }
}

async function submit_brand_info(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        const responseData = await response.json();
        if (responseData.reroute_location) {
               const swalWithBootstrapButtons = Swal.mixin({
              customClass: {
                confirmButton: "button_popup_design",
                cancelButton: "btn btn-danger"
              },
              buttonsStyling: false
            });

            swalWithBootstrapButtons.fire({
              text: "تم أنشاء كلمه المرور الجديده",
              showCancelButton: false,
              confirmButtonText: "تأكيد",
              reverseButtons: false,
              animation:false
            }).then((result) => {
              if (result.isConfirmed) {
                    window.location.href = responseData.reroute_location;
              } else if (
                /* Read more about handling dismissals below */
                result.dismiss === Swal.DismissReason.cancel
              ) {
                window.location.href = responseData.reroute_location;
              }else{
              window.location.href = responseData.reroute_location;
              }
            });
        }
    } catch (error) {
        console.error('Error:', error);
    }
}


