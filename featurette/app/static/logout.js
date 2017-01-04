$(document).ready(function() {
    $(document).on('click', '#logout', function(event) {
        $.ajax({
            url: 'http://localhost:5000/api/v1/logout',
            type: 'POST',
            success: function(data){
                console.log('Logged out');
                location.reload();
            }
        });
    });
});
