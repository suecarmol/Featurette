$(document).ready(function(){
    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
    $('#clients_id').addClass('active');
    $('#home_id').removeClass('active');
    $('#users_id').removeClass('active');
    $('#product_areas_id').removeClass('active');
});
