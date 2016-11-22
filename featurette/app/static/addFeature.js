$( document ).ready(function() {

	document.getElementById("target-date").flatpickr({
		minDate: "today",
		maxDate: "2050-12-31",
		enableTime: false,
		altInput: true
	});

	$('.ui.form').form({
    	fields: {
			request_title: {
        		identifier: 'request_title',
        		rules: [
          			{
            			type   : 'empty',
            			prompt : 'Please enter the title of the feature request'
          			}
        		]
      		},
			request_description: {
				identifier: 'request_description',
				rules: [
			  		{
			    		type: 'empty',
			    		prompt: 'Please enter the description of the feature request'
			  		},
					{
			    		type: 'minLength[10]',
			    		prompt: 'Your description has to have at least 10 characters'
			  		}
				]
			},
			client_priority: {
				identifier: 'client_priority',
				rules: [
					{
						type: 'empty',
						prompt: 'Please enter a priority'
					},
					{
						type: 'integer[1..100000000]',
						prompt: 'Number must be a positive integer'
					}
				]
			},
			target_date: {
				identifier: 'target_date',
				rules: [
					{
						type: 'empty',
						prompt: 'Please enter a date'
					}
				]
			},
			ticket_url: {
				identifier: 'ticket_url',
				rules: [
					{
						type: 'empty',
						prompt: 'Please enter a URL'
					},
					{
						type: 'url',
						prompt: 'The content must be a valid URL'
					}
				]
			},
			client: {
				identifier: 'client',
				rules: [
					{
						type:'empty',
						prompt: 'Please select a client'
					}
				]
			},
			product_area: {
				identifier: 'product_area',
				rules: [
					{
						type: 'empty',
						prompt: 'Please select a product area'
					}
				]
			}
		}
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
});
