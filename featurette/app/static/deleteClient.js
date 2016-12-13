$(document).ready(function() {

    $( document ).ajaxError(function( event, jqxhr, settings, exception ) {
        if ( jqxhr.status== 401 ) {
            //$( "div.log" ).text( "Triggered ajaxError handler." );
            window.location = '/login';
        }
    });

    $(document).on('click', '.delete', function(event) {
        var id = $(this).attr('value');
        $.ajax({
            url: '/api/v1/client/' + id,
            type: 'DELETE',
            success: function(data){
                console.log('Client deleted successfully');
                location.reload();
            }
        });
    });
});
