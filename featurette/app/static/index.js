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
        console.log("Feature Request");
        console.log(data);
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

    function FeatureRequestViewModel() {
        // Data
        var self = this;
        self.features = ko.observableArray([]);
        console.log("Sending requests...");
        $.getJSON("/api/v1/featureRequests", function(response) {
            console.log("Request sent...");
            console.log(response[0]);
            var mappedFeatures = $.map(response[0], function(item) { return new FeatureRequest(item) });
            console.log(mappedFeatures);
            self.features(mappedFeatures);

        });

        self.view_date_finished = ko.computed(function() {
        if (self.date_finished() == null)
          return '-';

        return self.date_finished();
      });
    }
    ko.applyBindings(new FeatureRequestViewModel());

});
