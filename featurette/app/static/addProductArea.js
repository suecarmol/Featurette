$(document).ready(function(){

	$( document ).ajaxError(function( event, jqxhr, settings, exception ) {
        if ( jqxhr.status== 401 ) {
            //$( "div.log" ).text( "Triggered ajaxError handler." );
            window.location = '/login';
        }
    });

    //Adding product area
	$('#submit').click(function(){
        var product_area = $('#product_area_name').val();
        if(product_area !== undefined || $.trim(product_area)){
			$.ajax({
	            url: '/api/v1/productAreas',
	            type: "POST",
	            data: {product_area_name : product_area},
	            success: function(data){
	                console.log('Product Area inserted successfully');
	            },
	            error: function(xhr,err){
	                console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
	                console.log("responseText: "+xhr.responseText);
	            }
	        });
		}
	});

});
