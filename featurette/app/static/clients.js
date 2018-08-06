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

    function Client(data) {
        // console.log("Client: ");
        // console.log(data.name);
        this.id = ko.observable(data.id);
        this.client_name = ko.observable(data.name);
    }


    function ClientViewModel() {
        // Data
        var self = this;
        self.clients = ko.observableArray([]);
        self.id = ko.observable(0);
        self.client_name = ko.observable('');

        self.getClients = function() {
            $.getJSON("/api/v1/clients", function(response) {
                var mappedClients = $.map(response, function(item) {
                    return new Client(item)
                });

            self.clients(mappedClients);

            });
        }

        self.addClient = function(){
            if( $('.ui.form').form('is valid')) {
                $.ajax({
                    url: "/api/v1/clients",
                    type: "POST",
                    data: { client_name: self.client_name() },
                    success: function (response) {
                        console.log("Client was added successfully... returning to clients view");
                        window.location.href = "/clients?message=Client was added successfully";
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

        self.deleteClient = function(row){
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
                        url: '/api/v1/client/' + row.id(),
                        type: 'DELETE',
                        success: function(data){
                            console.log('Client deleted successfully');
                            self.clients.remove(row);
                            message = "Client deleted successfully";
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

        self.editClient = function(row){
            console.log("Editing " + row.id());
            window.location = '/editClient?id=' + row.id();
        }

        self.getClient = function(id){
            $.getJSON("/api/v1/client/" + id, function(response) {
                self.client_name(response.name)
                self.id(response.id)
            });
        }

        self.updateClient = function(){
            if( $('.ui.form').form('is valid')) {
                console.log("Updating: " + self.id());
                $.ajax({
                    url: '/api/v1/client/'+ self.id(),
                    type: 'PUT',
                    data: {client_name: self.client_name()},
                    success: function(data){
                        console.log('Client updated successfully');
                        window.location.href = "/clients?message=Client updated successfully";
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

        if (window.location.pathname == '/clients'){
            self.getClients();
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

        if(window.location.pathname == '/editClient'){

            var id = getUrlParameter('id');
            console.log("Id transfered from Clients: " + id);
            self.getClient(id);
        }

        $('.ui.form').form({
            inline: true,
            fields: {
                client_name: {
                    identifier: 'client_name',
                    rules: [
                        {
                            type: 'empty',
                            prompt: 'Please enter a client'
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
    ko.applyBindings(new ClientViewModel());

});
