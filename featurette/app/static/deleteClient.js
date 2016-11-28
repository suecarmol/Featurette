$(document).ready(function() {
    $(document).on('click', '.delete', function(event) {
        var id = $(this).attr('value');
        $.ajax({
            url: 'http://localhost:5000/api/v1/client/' + id,
            type: 'DELETE',
            success: function(data){
                console.log('Client deleted successfully');
                location.reload();
            }
        });
    });
});
