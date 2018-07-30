$(document).ready(function() {

    $('.ui.secondary.pointing.menu')
        .on('click', '.item', function() {
            if(!$(this).hasClass('dropdown')) {
                $(this)
                .addClass('active')
                .siblings('.item')
                .removeClass('active');
            }
        });


    function ProductAreaViewModel() {
        // Data
        var self = this;
        self.productAreas = ko.observableArray([]);

        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/api/v1/productAreas",
            success: function (data) {
                //Here you map and create a new instance of userDetailVM
                console.log("Data: ");
                console.log(data);
                var observableData = ko.mapping.fromJS(data);
                var array = observableData();
                console.log("Array:");
                console.log(array);
                self.productAreas(array);
            }
        });

        console.log("Product Areas:");
        console.log(self.productAreas);

    }

    function ProductArea(data) {
        console.log("ProductArea");
        console.log(data.name);
        this.name = ko.observable(data.name);
    }

    ko.applyBindings(new ProductAreaViewModel(), document.getElementById('productAreasTable'));

});
