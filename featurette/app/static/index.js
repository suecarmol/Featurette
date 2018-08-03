$(document).ready(function() {

    //this is to activate the table sort only on /
    if (window.location.pathname == '/'){
        $('table').tablesort();
    }
    else{
        document.getElementById("target_date").flatpickr({
    		minDate: "today",
    		maxDate: "2050-12-31",
    		enableTime: false,
    		altInput: true
        });
    }

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

        self.getFeatures = function(){
            console.log("Sending getFeatures...");
            $.getJSON("/api/v1/featureRequests", function(response) {
                // console.log(response);
                var mappedFeatures = $.map(response, function(item) {
                    return new FeatureRequest(item)
                });
                self.features(mappedFeatures);
            });

            // console.log(self.features);
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

            // console.log(self.productAreas);
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

            // console.log(self.clients);
        }

        self.addFeature = function(){
            console.log("client_id: " + self.client_id() + ", product_area_id: " + self.product_area_id())
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
                    window.location.href = "/";
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
            });
        }

        self.finishFeature = function(row){
            console.log("Finishing feature request for id: " + row.id());
            if (confirm("Are you sure you want to mark this request as finished?")) {
                $.ajax({
                    url: '/api/v1/finishFeature/' + row.id(),
                    type: 'POST',
                    success: function(data){
                        console.log('Feature request marked as finished');
                    }
                });
            }
        }

        self.deleteFeature = function(row){
            console.log("DELETE command for id: " + row.id());

            if (confirm("Are you sure you want to delete this feature request?")) {
                $.ajax({
                    url: '/api/v1/featureRequest/' + row.id(),
                    type: 'DELETE',
                    success: function(data){
                        console.log('Feature request deleted successfully');
                        self.features.remove(row);
                    }
                });
            }
        }

        if (window.location.pathname == '/addFeature'){
            self.getProductAreas();
            self.getClients();
        }
        else{
            self.getFeatures();
        }
    }


    ko.cleanNode($("body")[0]);
    var viewModel = new FeatureRequestViewModel();
    ko.applyBindings(viewModel);

});
