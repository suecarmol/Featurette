$(document).ready(function(){

    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : sParameterName[1];
            }
        }
    };

    var id = getUrlParameter('id');

    $( document ).ajaxError(function( event, jqxhr, settings, exception ) {
        if ( jqxhr.status== 401 ) {
            //$( "div.log" ).text( "Triggered ajaxError handler." );
            window.location = '/login';
        }
    });

    $.ajax({
        url: 'http://localhost:5000/api/v1/productArea/' + id,
        type: 'GET',
        success(data){
            var name = document.getElementById('product_area_name').value = data.name;
            var id = document.getElementById('product_area_id').value = data.id;
        }

    });


    $('#submit').click(function(){
        console.log('Submitting! Such submit!');
        var product_area_id = $('#product_area_id').val();
        var product_area = $('#product_area_name').val();
        console.log(product_area_id);
        console.log(product_area);
        $.ajax({
            url: 'http://localhost:5000/api/v1/productArea/'+ product_area_id,
            type: 'PUT',
            data: {product_area_name : product_area},
            success: function(data){
                console.log('Product Area updated successfully');
            },
            error: function(xhr,err){
                console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
                console.log("responseText: "+xhr.responseText);
            }
        });
	});

});
