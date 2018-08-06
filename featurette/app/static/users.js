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
                    window.location.href = "/users?message=User was added successfully";
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
                        message = "User deleted successfully";
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
        }

        self.editUser = function(row){
            console.log("Editing " + row.id());
            window.location = '/editUser?id=' + row.id();
        }

        self.getUser = function(id){
            $.getJSON("/api/v1/user/" + id, function(response) {
                self.username(response.username)
                self.email(response.email)
                self.password(response.password)
                self.id(response.id)
            });
        }

        self.updateUser = function(){
            console.log("Updating: " + self.id());
            $.ajax({
                url: '/api/v1/user/'+ self.id(),
                type: 'PUT',
                data: {username: self.username(), email: self.email(), password: self.password()},
                success: function(data){
                    console.log('User updated successfully');
                    window.location.href = "/users?message=User updated successfully";
                },
                error: function(xhr,err){
                    console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
                    console.log("responseText: "+xhr.responseText);
                }
            });
        }

        if(window.location.pathname == '/editUser'){

            var id = getUrlParameter('id');
            console.log("Id transfered from Users: " + id);
            self.getUser(id);
        }

        if (window.location.pathname == '/users'){
            self.getUsers();
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

        // console.log("Users: ");
        // console.log(self.users);
    }

    ko.cleanNode($("body")[0]);
    ko.applyBindings(new UserViewModel());

});
