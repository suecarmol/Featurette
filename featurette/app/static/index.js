 $(document).ready(function() {

    //redirect to login when a 401 forbidden error is triggered
    $( document ).ajaxError(function( event, jqxhr, settings, exception ) {
        if ( jqxhr.status== 401 ) {
            window.location = '/login?message=Please log in before you can access the information';
        }
    });

    var calendar = null;

    //this is to activate the table sort only on /
    if (window.location.pathname == '/'){
        $('table').tablesort();
    }
    else{
        calendar = new Flatpickr(document.getElementById("target_date"))
    	calendar.config.minDate = "today";
    	calendar.config.maxDate = "2050-12-31";
    	calendar.config.enableTime = false;
    	calendar.config.altInput = true;
        calendar.config.altFormat = "F j, Y";
        calendar.config.dateFormat = "Y-m-d H:i";

    }

    var message = null;

    $('.message').hide();

    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });

    $('.ui.secondary.pointing.menu')
        .on('click', '.item', function() {
            if(!$(this).hasClass('dropdown')) {
                $(this)
                .addClass('active')
                .siblings('.item')
                .removeClass('active');
            }
        });

    function FeatureRequest(data) {

        if(data != null){
            // console.log("Feature Request");
            // console.log(data);
            this.id = ko.observable(data.id);
            this.title = ko.observable(data.title);
            this.description = ko.observable(data.description);
            this.client_id = ko.observable(data.client_id);
            this.client_name = ko.observable(data.client_name);
            this.client_priority = ko.observable(data.client_priority);
            this.product_area_id = ko.observable(data.product_area_id);
            this.product_area_name = ko.observable(data.product_area_name);
            this.user_id = ko.observable(data.user_id);
            this.username = ko.observable(data.username);
            this.target_date = ko.observable(data.target_date);
            this.ticket_url = ko.observable(data.ticket_url);
            this.date_finished = ko.observable(data.date_finished);
            this.is_finished = ko.observable(data.is_finished);
        }
    }

    function ProductArea(data) {
        // console.log("ProductArea: ");
        // console.log(data.name);
        this.id = ko.observable(data.id);
        this.product_area_name = ko.observable(data.name);
    }

    function Client(data) {
        // console.log("Client: ");
        // console.log(data.name);
        this.id = ko.observable(data.id);
        this.client_name = ko.observable(data.name);
    }

    function FeatureRequestViewModel() {
        // Data
        var self = this;
        self.id = ko.observable(0);
        self.features = ko.observableArray();
        self.productAreas = ko.observableArray();
        self.clients = ko.observableArray();
        self.title = ko.observable("");
        self.description = ko.observable("");
        self.client_id = ko.observable(0);
        self.client_priority = ko.observable(0);
        self.product_area_id = ko.observable(0);
        self.target_date = ko.observable("");
        self.ticket_url = ko.observable("");
        self.is_finished = ko.observable(false);

        self.getFeatures = function(){
            console.log("Sending getFeatures...");
            $.getJSON("/api/v1/featureRequests", function(response) {
                // console.log(response);
                var mappedFeatures = $.map(response, function(item) {
                    return new FeatureRequest(item)
                });
                self.features(mappedFeatures);
            });

        }

        self.getProductAreas = function(){
            console.log("Sending getProductAreas...");
            $.getJSON("/api/v1/productAreas", function(response) {
                // console.log(response);
                var mappedProducts = $.map(response, function(item) {
                    return new ProductArea(item)
                });
                self.productAreas(mappedProducts);
            });

        }

        self.getClients = function(){
            console.log("Sending getClients...");
            $.getJSON("/api/v1/clients", function(response) {
                // console.log(response);
                var mappedClients = $.map(response, function(item) {
                    return new Client(item)
                });
                self.clients(mappedClients);
            });

        }

        self.addFeature = function(){
            if( $('.ui.form').form('is valid')) {
                $.ajax({
                    url: "/api/v1/featureRequests",
                    type: "POST",
                    data: { title: self.title(), description: self.description(),
                            client_id: self.client_id(), client_priority: self.client_priority(),
                            product_area_id: self.product_area_id(), target_date: self.target_date(),
                            ticket_url: self.ticket_url() },
                    success: function (response) {
                        console.log("Feature request was added successfully... returning to features view");
                        // console.log(response);
                        window.location.href = "/?message=Feature request was added successfully";
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        console.log(xhr.status);
                        console.log(thrownError);
                    }
                });
            }
            else{
                console.log("Form is not valid");
            }
        }

        self.finishFeature = function(row){
            console.log("Finishing feature request for id: " + row.id());

            $('#finishModal').modal({
                onHide: function(){
                    console.log('hidden');
                },
                onShow: function(){
                    console.log('shown');
                },
                onApprove: function() {
                    console.log('Approve');
                    $.ajax({
                        url: '/api/v1/finishFeature/' + row.id(),
                        type: 'POST',
                        success: function(data){
                            console.log('Feature request marked as finished');
                            message = "Feature request marked as finished";
                            $('.message').show();
                            $('#messageSpace').text(message);
                            $('.message .close')
                            .on('click', function() {
                                $(this)
                                .closest('.message')
                                .transition('fade');
                            });
                        }
                    });
                }
            }).modal('show');
        }

        self.isFeatureFinished = function(){
            return self.is_finished();
        }

        self.deleteFeature = function(row){
            console.log("DELETE command for id: " + row.id());

            $('#deleteModal').modal({
                onHide: function(){
                    console.log('hidden');
                },
                onShow: function(){
                    console.log('shown');
                },
                onApprove: function() {
                    console.log('Approve');
                    $.ajax({
                        url: '/api/v1/featureRequest/' + row.id(),
                        type: 'DELETE',
                        success: function(data){
                            console.log('Feature request deleted successfully');
                            self.features.remove(row);
                            message = "Feature request deleted successfully";
                            $('.message').show();
                            $('#messageSpace').text(message);
                            $('.message .close')
                            .on('click', function() {
                                $(this)
                                .closest('.message')
                                .transition('fade');
                            });
                        }
                    });
                }
            }).modal('show');

        }

        self.editFeature = function(row){
            console.log("Editing " + row.id());
            window.location = '/editFeature?id=' + row.id();
        }

        self.getFeature = function(id){
            $.getJSON("/api/v1/featureRequest/" + id, function(response) {
                // console.log(response);
                self.title(response.title)
                self.description(response.description)
                self.client_id(response.client_id)
                self.client_priority(response.client_priority)
                self.product_area_id(response.product_area_id)
                self.target_date(response.target_date)
                self.ticket_url(response.ticket_url)
                self.id(response.id)
                calendar.setDate(self.target_date(), 'Y-m-d h:i')
            });
        }

        self.updateFeature = function(){
            if( $('.ui.form').form('is valid')) {
                console.log("Updating: " + self.id());
                $.ajax({
                    url: '/api/v1/featureRequest/'+ self.id(),
                    type: 'PUT',
                    data: {title: self.title(), description: self.description(),
                            client_id: self.client_id(), client_priority: self.client_priority(),
                            product_area_id: self.product_area_id(), target_date: self.target_date(),
                            ticket_url: self.ticket_url()},
                    success: function(data){
                        console.log('Feature request updated successfully');
                        window.location.href = "/?message=Feature request was updated successfully";
                    },
                    error: function(xhr,err){
                        console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
                        console.log("responseText: "+xhr.responseText);
                    }
                });
            }
            else{
                console.log("Form is not valid");
            }
        }


        if (window.location.pathname == '/addFeature'){
            self.getProductAreas();
            self.getClients();
        }
        else if (window.location.pathname == '/editFeature'){
            self.getProductAreas();
            self.getClients();
            var id = getUrlParameter('id');
            console.log("Id transfered from Feature requests: " + id);
            self.getFeature(id);
        }
        else{
            self.getFeatures();
            message = getUrlParameter('message');

            if(message != null){
                $('.message').show();
                $('#messageSpace').text(message);
                $('.message .close')
                .on('click', function() {
                    $(this)
                    .closest('.message')
                    .transition('fade');
                });
            }
        }
    }

    $('.ui.form').form({
        inline: true,
        fields: {
            title: {
                identifier: 'title',
                rules: [
                    {
                        type   : 'empty',
                        prompt : 'Please enter the title of the feature request'
                    }
                ]
            },
            description: {
                identifier: 'description',
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

    function getUrlParameter(sParam) {
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
    }

    ko.cleanNode($("body")[0]);
    var viewModel = new FeatureRequestViewModel();
    ko.applyBindings(viewModel);

});
