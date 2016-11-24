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
		//TODO: get form values and pass them to data
		$.ajax({
			url: 'http://localhost:5000/api/v1/featureRequest',
            type: "POST",
			data: {},
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
