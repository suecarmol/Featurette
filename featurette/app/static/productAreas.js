$(document).ready(function(){
    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
    $('#clients_id a').removeClass('active');
    $('#home_id a').removeClass('active');
    $('#users_id a').removeClass('active');
    $('#product_areas_id a').addClass('active');
});
