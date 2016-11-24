$(document).ready(function(){

    //Adding product area
	$('#submit').click(function(){
        var product_area = $('#product_area_name').val();
        console.log(product_area);
        $.ajax({
            url: 'http://localhost:5000/api/v1/productAreas',
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
	});
    
});
