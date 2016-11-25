$( document ).ready(function() {

	document.getElementById("target-date").flatpickr({
		minDate: "today",
		maxDate: "2050-12-31",
		enableTime: false,
		altInput: true
	});

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

	//Adding feature request
	$('#submit').click(function(){
		var request_title = $('#request_title').val();
		var request_description = $('#request_description').val();
		var client = $('#client').val();
		var client_priority = $('#client_priority').val();
		var target_date = $('#target-date').val();
		var product_area = $('#product_area').val();
		var ticket_url = $('#ticket_url').val();
		$.ajax({
			url: 'http://localhost:5000/api/v1/featureRequest',
            type: "POST",
			data: {title: request_title, description: request_description,
				   client_id: client, client_priority: client_priority,
				   target_date: target_date, product_area_id: product_area,
			       ticket_url: ticket_url},
			success: function(data){
                console.log('Feature request inserted successfully');
            },
            error: function(xhr,err){
                console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
                console.log("responseText: "+xhr.responseText);
            }

		});
	});
});
