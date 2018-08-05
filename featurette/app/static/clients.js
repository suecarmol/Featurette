$(document).ready(function() {

    //redirect to login when a 401 forbidden error is triggered
    $( document ).ajaxError(function( event, jqxhr, settings, exception ) {
        if ( jqxhr.status== 401 ) {
            //$( "div.log" ).text( "Triggered ajaxError handler." );
            window.location = '/login';
        }
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
            $.ajax({
                url: "/api/v1/clients",
                type: "POST",
                data: { client_name: self.client_name() },
                success: function (response) {
                    console.log("Client was added successfully... returning to clients view");
                    console.log(response)
                    window.location.href = "/clients";
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
            });
        }

        self.deleteClient = function(row){
            console.log("DELETE command for id: " + row.id());

            if (confirm("Are you sure you want to delete this client?")) {
                $.ajax({
                    url: '/api/v1/client/' + row.id(),
                    type: 'DELETE',
                    success: function(data){
                        console.log('Client deleted successfully');
                        self.clients.remove(row);
                    }
                });
            }
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
            console.log("Updating: " + self.id());
            $.ajax({
                url: '/api/v1/client/'+ self.id(),
                type: 'PUT',
                data: {client_name: self.client_name()},
                success: function(data){
                    console.log('Client updated successfully');
                    window.location.href = "/clients";
                },
                error: function(xhr,err){
                    console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
                    console.log("responseText: "+xhr.responseText);
                }
            });
        }

        if (window.location.pathname == '/clients'){
            self.getClients();
        }

        if(window.location.pathname == '/editClient'){
            var getUrlParameter = function getUrlParameter(sParam) {
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
            };

            var id = getUrlParameter('id');

            console.log("Id transfered from Clients: " + id);

            self.getClient(id);
        }
    }

    ko.cleanNode($("body")[0]);
    ko.applyBindings(new ClientViewModel());

});
