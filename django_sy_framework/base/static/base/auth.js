$('#btn_google_auth').click(function() {window.onfocus = function(){window.location.reload();}})

$('#btn_toggle_login_box').click(function(event) {
    $('#login_box').toggle();
    $('#registration_box').hide();
});
$('#btn_toggle_registration_box').click(function(event) {
    $('#registration_box').toggle();
    $('#login_box').hide();
});

$('#login_button').click(function(event) {
    let form = event.target.form;
    $.ajax({
        url: URL_LOGIN,
        headers: {
            "X-CSRFToken": CSRF_TOKEN,
        },
        dataType: 'json',
        data: $(form).serialize(),
        success: function(result) {
            if (result.success) {
                invert_status_fields(form);
                window.location = window.location;
            } else {
                $('#login_bad_message').text('Неправильный пароль или пользователь не существует');
                $('#login_bad_message').removeClass('d-none');
            }
        },
        error: function(jqxhr, a, b) {
            console.log('error');
            console.log(jqxhr.responseText);
        },
        method: "post"
    });
});
$('#registrate_button').click(function(event) {
    let form = event.target.form;
    $.ajax({
        url: URL_REGISTRATION,
        headers: {
            "X-CSRFToken": CSRF_TOKEN,
        },
        dataType: 'json',
        data: $(form).serialize(),
        success: function(result) {
            invert_status_fields(form);
            window.location = window.location;
        },
        statusCode: {
            400: function(xhr) {
                clear_status_fields(form);
                set_invalid_field(form, xhr.responseJSON);
            },
        },
        method: "post"
    });
});