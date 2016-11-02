$(document).ready(function(){
    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
    $('.home_id a').addClass('active');
    $('.users_id a').removeClass('active');
    $('.clients_id a').removeClass('active');
    $('.product_areas_id a').removeClass('active');
});
