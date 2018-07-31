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
        self.product_area_name = ko.observable('');

        self.getProductAreas = function() {
            $.ajax({
                type: "GET",
                dataType: "json",
                url: "api/v1/productAreas",
                success: function (data) {
                    console.log("Data: ");
                    console.log(data);
                    for(d = 0; d < data.length; d++){
                        self.productAreas.push(data[d]);
                    }
                }
            });
        }

        self.addProductArea = function(){
            $.ajax({
                url: "api/v1/productAreas",
                type: "POST",
                data: { product_area_name: self.product_area_name() },
                success: function (response) {
                    console.log("Product was added successfully... returning to product area");
                    console.log(response)
                    window.location.href = "/productAreas";
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
            });
        }

        self.getProductAreas();

        // console.log("Product Areas: ");
        // console.log(self.productAreas);
    }

    function ProductArea(data) {
        console.log("ProductArea: ");
        console.log(data.product_area_name);
        this.product_area_name = ko.observable(data.product_area_name);
    }

    ko.cleanNode($("body")[0]);
    ko.applyBindings(new ProductAreaViewModel());

});
