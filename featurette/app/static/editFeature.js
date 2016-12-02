$(document).ready(function(){

    document.getElementById("target-date").flatpickr({
		minDate: "today",
		maxDate: "2050-12-31",
		enableTime: false,
		altInput: true
	});

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

    //get clients
	$.getJSON({
		url: 'http://localhost:5000/api/v1/clients',
		dataType: 'json',
        success: function(data){
			var client_select = document.getElementById('client');
			$.each(data, function(index, element) {
				var opt = document.createElement('option');
				opt.setAttribute('value', element.id);
				opt.textContent= element.name;
				client_select.appendChild(opt);
			});
		}
	});

	//get product areas
	$.getJSON({
		url: 'http://localhost:5000/api/v1/productAreas',
		dataType: 'json',
        success: function(data){
			var product_area_select = document.getElementById('product_area');
			$.each(data, function(index, element) {
				var opt = document.createElement('option');
				opt.setAttribute('value', element.id);
				opt.textContent = element.name;
				product_area_select.appendChild(opt);
			});
		}
	});

    $.ajax({
        url: 'http://localhost:5000/api/v1/featureRequest/' + id,
        type: 'GET',
        success(data){
            var id = document.getElementById('feature_request_id').value = data.id;
            var title = document.getElementById('request_title').value = data.title;
            var description = document.getElementById('request_description').value = data.description;
            var client_id = document.getElementById('current_client').text = data.client_id;
            var client_priority = document.getElementById('client_priority').value = data.client_priority;
            var target_date = document.getElementById('target-date').value = data.target_date;
            var product_area = document.getElementById('current_product_area').text = data.product_area_id;
            var ticket_url = document.getElementById('ticket_url').value = data.ticket_url;
        }

    });


    $('#submit').click(function(){
        console.log('Submitting feature!');
        var feature_request_id = $('#feature_request_id').val();
        var title = $('#request_title').val();
        var description = $('#request_description').val();
        var client_id = $('#client').val();
        var client_priority = $('#client_priority').val();
        var target_date = $('#target-date').val();
        var product_area_id = $('#product_area').val();
        var ticket_url = $('#ticket_url').val();
        console.log(feature_request_id);
        console.log(title);
        $.ajax({
            url: 'http://localhost:5000/api/v1/featureRequest/'+ feature_request_id,
            type: 'PUT',
            data: {title : title, description : description, client_id : client_id,
            client_priority : client_priority, target_date : target_date, product_area_id : product_area_id,
            ticket_url : ticket_url},
            success: function(data){
                console.log('Feature request updated successfully');
            },
            error: function(xhr,err){
                console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
                console.log("responseText: "+xhr.responseText);
            }
        });
	});

});
