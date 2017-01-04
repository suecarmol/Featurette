$(document).ready(function(){

	function validateEmail(mail){
		if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail)){
			return true;
		}
		return false;
	}


	//redirected when unauthorized
	$( document ).ajaxError(function( event, jqxhr, settings, exception ) {
        if ( jqxhr.status== 401 ) {
            window.location = '/login';
        }
    });

    //Adding user
	$('#submit').click(function(){
		console.log('Submitting user...');
        var username = $('#username').val();
        var email = $('#email').val();
        var password = $('#password').val();
		if((username !== undefined || $.trim(username)) ||
			(email !== undefined || $.trim(email)) ||
			(password !== undefined || $.trim(password))){
			if(validateEmail(email)){
				console.log('Valid email');
				$.ajax({
		            url: '/api/v1/users',
		            type: "POST",
		            data: {username : username, email : email, password : password},
		            success: function(data){
		                console.log('User inserted successfully');
						console.log(data);
		            },
		            error: function(xhr,err){
		                console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
		                console.log("responseText: "+xhr.responseText);
		            }
		        });
			}
		}
	});

});
