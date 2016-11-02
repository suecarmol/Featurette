$(document).ready(function(){
    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
    $('#users_id').addClass('active');
    $('#clients_id').removeClass('active');
    $('#home_id').removeClass('active');
    $('#product_areas_id').removeClass('active');
});
