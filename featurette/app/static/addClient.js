$(document).ready(function(){

    //Adding client
	$('#submit').click(function(){
        var client_name = $('#client_name').val();
        console.log(client_name);
        $.ajax({
            url: 'http://localhost:5000/api/v1/clients',
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
