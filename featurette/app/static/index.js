$(document).ready(function() {

    $('table').tablesort();
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
            this.client_priority = ko.observable(data.client_priority);
            this.product_area_id = ko.observable(data.product_area_id);
            this.user_id = ko.observable(data.user_id);
            this.target_date = ko.observable(data.target_date);
            this.ticket_url = ko.observable(data.ticket_url);
            this.date_finished = ko.observable(data.date_finished);
        }
    }

    function FeatureRequestViewModel() {
        // Data
        var self = this;
        self.id = ko.observable(0);
        self.features = ko.observableArray();

        self.getFeatures = function(){
            console.log("Sending getFeatures...");
            $.getJSON("/api/v1/featureRequests", function(response) {
                // var res = JSON.stringify(response);
                console.log(response);
                var mappedFeatures = $.map(response, function(item) {
                    return new FeatureRequest(item)
                });
                self.features(mappedFeatures);
            });
        }

        self.deleteFeature = function(row){
            console.log("DELETE command for id: " + row.id());
            $.ajax({
                url: '/api/v1/featureRequest/' + row.id(),
                type: 'DELETE',
                success: function(data){
                    console.log('Feature request deleted successfully');
                    self.features.remove(row);
                }
            });
        }

        self.getFeatures();
    }


    ko.cleanNode($("body")[0]);
    var viewModel = new FeatureRequestViewModel();
    ko.applyBindings(viewModel);

});
