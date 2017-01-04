$(document).ready(function() {
    $(document).on('click', '.finish', function(event) {
        var id = $(this).attr('value');
        $.ajax({
            url: 'http://localhost:5000/api/v1/finishFeature/' + id,
            type: 'POST',
            success: function(data){
                console.log('Feature request finished successfully');
                location.reload();
            }
        });
    });
});
