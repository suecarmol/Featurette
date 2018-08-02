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

    function User(data) {
        // console.log("User: ");
        // console.log(data.name);
        this.id = ko.observable(data.id);
        this.username = ko.observable(data.username);
        this.email = ko.observable(data.email);
    }


    function UserViewModel() {
        // Data
        var self = this;
        self.users = ko.observableArray([]);
        self.id = ko.observable(0);
        self.username = ko.observable('').extend({ required: { params: true, message: 'The username is required.' }});
        self.email = ko.observable('').extend({ email: true, required: { params: true, message: 'This field is required.' } });
        self.password = ko.observable('').extend({ required: { params: true, message: 'The password is required.' }});
        self.repeat_password = ko.observable('').extend({ equal: self.password });

        self.getUsers = function() {
            $.getJSON("/api/v1/users", function(response) {
                var mappedUsers = $.map(response, function(item) {
                    return new User(item)
                });

            self.users(mappedUsers);

            });
        }


        self.addUser = function(){
            $.ajax({
                url: "/api/v1/users",
                type: "POST",
                data: { username: self.username(), email: self.email(), password: self.password() },
                success: function (response) {
                    console.log("User was added successfully... returning to users view");
                    // console.log(response);
                    window.location.href = "/users";
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
            });
        }

        self.deleteUser = function(row){
            console.log("DELETE command for id: " + row.id());

            if (confirm("Are you sure you want to delete this user?")) {
                $.ajax({
                    url: '/api/v1/user/' + row.id(),
                    type: 'DELETE',
                    success: function(data){
                        console.log('User deleted successfully');
                        self.users.remove(row);
                    }
                });
            }
        }

        if (window.location.pathname == '/users'){
            self.getUsers();
        }

        // console.log("Users: ");
        // console.log(self.users);
    }

    ko.cleanNode($("body")[0]);
    ko.applyBindings(new UserViewModel());

});
