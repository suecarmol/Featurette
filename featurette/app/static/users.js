$(document).ready(function(){
    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
    $('#users_id a').addClass('active');
    $('#clients_id a').removeClass('active');
    $('#home_id a').removeClass('active');
    $('#product_areas_id a').removeClass('active');
});
