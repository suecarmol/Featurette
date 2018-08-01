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
            $.ajax({
                url: '/api/v1/client/' + row.id(),
                type: 'DELETE',
                success: function(data){
                    console.log('Client deleted successfully');
                    self.clients.remove(row);
                }
            });
        }


        self.getClients();

        // console.log("Clients: ");
        // console.log(self.clients);
    }

    ko.cleanNode($("body")[0]);
    ko.applyBindings(new ClientViewModel());

});
