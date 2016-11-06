$(document).ready(function(){
    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
    // $('.home_id a').addClass('active');
    // $('.users_id a').removeClass('active');
    // $('.clients_id a').removeClass('active');
    // $('.product_areas_id a').removeClass('active');
    $('.ui.secondary.pointing.menu')
    .on('click', '.item', function() {
      if(!$(this).hasClass('dropdown')) {
        $(this)
          .addClass('active')
          .siblings('.item')
            .removeClass('active');
      }
    });
});
