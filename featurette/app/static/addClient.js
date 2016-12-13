$(document).ready(function(){

	$( document ).ajaxError(function( event, jqxhr, settings, exception ) {
        if ( jqxhr.status== 401 ) {
            //$( "div.log" ).text( "Triggered ajaxError handler." );
            window.location = '/login';
        }
    });

    //Adding client
	$('#submit').click(function(){
        var client_name = $('#client_name').val();
        console.log(client_name);
        $.ajax({
            url: '/api/v1/clients',
            type: "POST",
            data: {client_name : client_name},
            success: function(data){
                console.log('Client inserted successfully');
            },
            error: function(xhr,err){
                console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
                console.log("responseText: "+xhr.responseText);
            }
        });
	});

});
