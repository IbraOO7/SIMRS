$(document).ready(function() {
    $('#Masuk').click(function() {
        $.ajax({
            url: '/login',
            type: 'POST',
            dataType: 'json',
            data: $('form').serialize(),
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
