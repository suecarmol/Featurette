$(document).ready(function() {

    //redirect to login when a 401 forbidden error is triggered
    $( document ).ajaxError(function( event, jqxhr, settings, exception ) {
        if ( jqxhr.status== 401 ) {
            //$( "div.log" ).text( "Triggered ajaxError handler." );
            window.location = '/login?message=Please log in before you can access the information';
        }
    });

    var message = null;

    $('.message').hide();

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
            if( $('.ui.form').form('is valid')) {
                $.ajax({
                    url: "/api/v1/productAreas",
                    type: "POST",
                    data: { product_area_name: self.product_area_name() },
                    success: function (response) {
                        console.log("Product was added successfully... returning to product areas");
                        // console.log(response)
                        window.location.href = "/productAreas?message=Product area was added successfully";
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

        self.deleteProductArea = function(row){
            console.log("DELETE command for id: " + row.id());

            $('.mini.modal').modal({
                onHide: function(){
                    console.log('hidden');
                },
                onShow: function(){
                    console.log('shown');
                },
                onApprove: function() {
                    console.log('Approve');
                    $.ajax({
                        url: '/api/v1/productArea/' + row.id(),
                        type: 'DELETE',
                        success: function(data){
                            console.log('Product area deleted successfully');
                            self.productAreas.remove(row);
                            message = "Product area deleted successfully";
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

        self.editProductArea = function(row){
            console.log("Editing " + row.id());
            window.location = '/editProductArea?id=' + row.id();
        }

        self.getProductArea = function(id){
            $.getJSON("/api/v1/productArea/" + id, function(response) {
                self.product_area_name(response.name)
                self.id(response.id)
            });
        }

        self.updateProductArea = function(){
            if( $('.ui.form').form('is valid')) {
                console.log("Updating: " + self.id());
                $.ajax({
                    url: '/api/v1/productArea/'+ self.id(),
                    type: 'PUT',
                    data: {product_area_name: self.product_area_name()},
                    success: function(data){
                        console.log('Product Area updated successfully');
                        window.location.href = "/productAreas?message=Product area was updated successfully";
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

        if (window.location.pathname == '/productAreas'){
            self.getProductAreas();
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

        if(window.location.pathname == '/editProductArea'){

            var id = getUrlParameter('id');
            console.log("Id transfered from Product Areas: " + id);
            self.getProductArea(id);
        }

        $('.ui.form').form({
            inline: true,
            fields: {
                product_area_name: {
                    identifier: 'product_area_name',
                    rules: [
                        {
                            type: 'empty',
                            prompt: 'Please enter a product area name'
                        },
                        {
                            type: 'minLength[2]',
                            prompt: 'The product area must be more than 2 characters long'
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

    }

    ko.cleanNode($("body")[0]);
    ko.applyBindings(new ProductAreaViewModel());

});
