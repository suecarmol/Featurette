$(document).ready(function(){
    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
    // $('#users_id a').addClass('active');
    // $('#clients_id a').removeClass('active');
    // $('#home_id a').removeClass('active');
    // $('#product_areas_id a').removeClass('active');
    $('.ui .item').on('click', function() {
       $('.ui .item').removeClass('active');
       $(this).addClass('active');
    });

    $( document ).ajaxError(function( event, jqxhr, settings, exception ) {
        if ( jqxhr.status== 401 ) {
            //$( "div.log" ).text( "Triggered ajaxError handler." );
            window.location = '/login';
        }
    });

    $.getJSON({
        url: 'http://localhost:5000/api/v1/users',
        dataType: 'json',
        success: function(data){
            $.each(data, function(index, element) {
                //getting the table body
                var tbody = document.getElementById('usersTable');

                //td information
                var tr = document.createElement('tr');
                var td_username = document.createElement('td');
                td_username.textContent= element.username;

                var td_email = document.createElement('td');
                td_email.textContent= element.email;

                //td actions
                var td_actions = document.createElement('td');
                td_actions.setAttribute('class', 'single line');

                var editButton = document.createElement('a');
                editButton.setAttribute('class', 'edit ui icon violet button');
                editButton.setAttribute('value', element.id);

                var editIcon = document.createElement('i');
                editIcon.setAttribute('class', 'edit icon');
                editButton.appendChild(editIcon);

                var deleteButton = document.createElement('a');
                deleteButton.setAttribute('class', 'delete ui icon red button');
                deleteButton.setAttribute('value', element.id);

                var deleteIcon = document.createElement('i');
                deleteIcon.setAttribute('class', 'delete icon');
                deleteButton.appendChild(deleteIcon);

                td_actions.appendChild(editButton);
                td_actions.appendChild(deleteButton);


                tr.appendChild(td_username);
                tr.appendChild(td_email);
                tr.appendChild(td_actions);
                tbody.appendChild(tr);

            });
        }
    });
    $(document).on('click', '.edit', function(event){
        var id = $(this).attr('value');
        window.location = '/editUser?id=' + id;
    });
});
