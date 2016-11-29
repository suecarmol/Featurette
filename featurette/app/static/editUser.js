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

    $.ajax({
        url: 'http://localhost:5000/api/v1/user/' + id,
        type: 'GET',
        success(data){
            var username = document.getElementById('username').value = data.username;
            var email = document.getElementById('email').value = data.email;
            var id = document.getElementById('user_id').value = data.id;
        }

    });


    $('#submit').click(function(){
        console.log('Submitting user!');
        var user_id = $('#user_id').val();
        var username = $('#username').val();
        var email = $('#email').val();
        var password = $('#password').val();
        console.log(user_id);
        console.log(username);
        $.ajax({
            url: 'http://localhost:5000/api/v1/user/'+ user_id,
            type: 'PUT',
            data: {username : username, email : email, password : password},
            success: function(data){
                console.log('User updated successfully');
            },
            error: function(xhr,err){
                console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
                console.log("responseText: "+xhr.responseText);
            }
        });
	});

});
