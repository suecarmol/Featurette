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

    function ProductArea(data) {
        // console.log("ProductArea: ");
        // console.log(data.name);
        this.id = ko.observable(data.id);
        this.product_area_name = ko.observable(data.name);
    }


    function ProductAreaViewModel() {
        // Data
        var self = this;
        self.productAreas = ko.observableArray([]);
        self.id = ko.observable(0);
        self.product_area_name = ko.observable('');

        self.getProductAreas = function() {
            $.getJSON("/api/v1/productAreas", function(response) {
                var mappedProducts = $.map(response, function(item) {
                    return new ProductArea(item)
                });

            self.productAreas(mappedProducts);

            });
        }

        self.addProductArea = function(){
            $.ajax({
                url: "/api/v1/productAreas",
                type: "POST",
                data: { product_area_name: self.product_area_name() },
                success: function (response) {
                    console.log("Product was added successfully... returning to product areas");
                    // console.log(response)
                    window.location.href = "/productAreas";
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
            });
        }

        self.deleteProductArea = function(row){
            console.log("DELETE command for id: " + row.id());
            $.ajax({
                url: '/api/v1/productArea/' + row.id(),
                type: 'DELETE',
                success: function(data){
                    console.log('Product area deleted successfully');
                    self.productAreas.remove(row);
                }
            });
        }

        self.getProductAreas();

        // console.log("Product Areas: ");
        // console.log(self.productAreas);
    }

    ko.cleanNode($("body")[0]);
    ko.applyBindings(new ProductAreaViewModel());

});
