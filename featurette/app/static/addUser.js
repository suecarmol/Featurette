$(document).ready(function(){

	$( document ).ajaxError(function( event, jqxhr, settings, exception ) {
        if ( jqxhr.status== 401 ) {
            //$( "div.log" ).text( "Triggered ajaxError handler." );
            window.location = '/login';
        }
    });

    //Adding user
	$('#submit').click(function(){
        var username = $('#username').val();
        var email = $('#email').val();
        var password = $('#password').val();
		if(username !== undefined && email !== undefined && password !== undefined){
			$.ajax({
	            url: '/api/v1/users',
	            type: "POST",
	            data: {username : username, email : email, password : password},
	            success: function(data){
	                console.log('User inserted successfully');
	            },
	            error: function(xhr,err){
	                console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
	                console.log("responseText: "+xhr.responseText);
	            }
	        });
		}
	});

});
