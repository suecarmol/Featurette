$(document).ready(function(){
    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
    $('#home_id').addClass('active');
    $('#users_id').removeClass('active');
    $('#clients_id').removeClass('active');
    $('#product_areas_id').removeClass('active');
});
