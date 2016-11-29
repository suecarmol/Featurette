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
        url: 'http://localhost:5000/api/v1/client/' + id,
        type: 'GET',
        success(data){
            var name = document.getElementById('client_name').value = data.name;
            var id = document.getElementById('client_id').value = data.id;
        }

    });


    $('#submit').click(function(){
        console.log('Submitting! Such submit!');
        var client_id = $('#client_id').val();
        var client = $('#client_name').val();
        console.log(client_id);
        console.log(client);
        $.ajax({
            url: 'http://localhost:5000/api/v1/client/'+ client_id,
            type: 'PUT',
            data: {client_name : client},
            success: function(data){
                console.log('Client updated successfully');
            },
            error: function(xhr,err){
                console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
                console.log("responseText: "+xhr.responseText);
            }
        });
	});

});
