$(document).ready(function(){
    $('.ui.form').form({
        fields: {
            client_name: {
                identifier: 'client_name',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter a client'
                    }
                ]
            }
        }
    });

    //Adding client
	$('#submit').click(function(){
        var client_name = $('#client_name').val();
        console.log(client_name);
        $.ajax({
            url: 'http://localhost:5000/api/v1/clients',
            type: "POST",
            data: client_name,
            success: window.location.replace("http://localhost:5000/clients"),
            error: function(xhr,err){
                console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
                console.log("responseText: "+xhr.responseText);
            }
        });
	});
});
