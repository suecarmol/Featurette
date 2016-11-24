$(document).ready(function(){

    //Adding user
	$('#submit').click(function(){
        var username = $('#username').val();
        var email = $('#email').val();
        var password = $('#password').val();
        $.ajax({
            url: 'http://localhost:5000/api/v1/users',
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
	});
    
});
