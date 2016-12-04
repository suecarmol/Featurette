$(document).ready(function(){

    $('table').tablesort();
    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
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

    $( document ).ajaxError(function( event, jqxhr, settings, exception ) {
        if ( jqxhr.status== 401 ) {
            //$( "div.log" ).text( "Triggered ajaxError handler." );
            window.location = '/login';
        }
    });

    $.getJSON({
        url: 'http://localhost:5000/api/v1/featureRequests',
        dataType: 'json',
        success: function(data){
            $.each(data, function(index, element) {
                //getting the table body
                var tbody = document.getElementById('featuresTable');

                //td information
                var tr = document.createElement('tr');

                var td_title = document.createElement('td');
                td_title.textContent= element.title;

                var td_description = document.createElement('td');
                td_description.textContent= element.description;

                var td_client_id = document.createElement('td');
                //getting client name
                $.getJSON({
                    url: 'http://localhost:5000/api/v1/client/' + element.client_id,
                    dataType: 'json',
                    success: function(data){
                        td_client_id.textContent= data.name;
                    }
                });

                var td_client_priority = document.createElement('td');
                td_client_priority.textContent= element.client_priority;

                var td_product_area = document.createElement('td');
                //getting product area
                $.getJSON({
                    url: 'http://localhost:5000/api/v1/productArea/' + element.product_area_id,
                    dataType: 'json',
                    success: function(data){
                        td_product_area.textContent= data.name;
                    }
                });

                var td_target_date = document.createElement('td');
                var date = new Date(element.target_date);
                month = date.getMonth() + 1;
                td_target_date.textContent= date.getDate() + '/' + month + '/' + date.getFullYear();

                var td_ticket_url = document.createElement('td');
                td_ticket_url.textContent= element.ticket_url;

                var td_user_id = document.createElement('td');
                //getting user
                $.getJSON({
                    url: 'http://localhost:5000/api/v1/user/' + element.user_id,
                    dataType: 'json',
                    success: function(data){
                        td_user_id.textContent= data.username;
                    }
                });

                //td actions
                var td_actions = document.createElement('td');
                td_actions.setAttribute('class', 'single line');

                var editButton = document.createElement('a');
                if(element.date_finished != null){
                    editButton.setAttribute('class', 'ui icon violet button disabled');
                }
                else{
                    editButton.setAttribute('class', 'edit ui icon violet button');
                    editButton.setAttribute('value', element.id);
                }

                var editIcon = document.createElement('i');
                editIcon.setAttribute('class', 'edit icon');
                editButton.appendChild(editIcon);

                var finishButton = document.createElement('button');
                if(element.date_finished != null){
                    finishButton.setAttribute('class', 'ui icon green button disabled');
                }
                else{
                    finishButton.setAttribute('class', 'finish ui icon green button');
                    finishButton.setAttribute('value', element.id);
                }

                var finishIcon = document.createElement('i');
                finishIcon.setAttribute('class', 'check icon');
                finishButton.appendChild(finishIcon);

                var deleteButton = document.createElement('button');
                deleteButton.setAttribute('class', 'delete ui icon red button');
                deleteButton.setAttribute('value', element.id);

                var deleteIcon = document.createElement('i');
                deleteIcon.setAttribute('class', 'delete icon');
                deleteButton.appendChild(deleteIcon);

                td_actions.appendChild(editButton);
                td_actions.appendChild(finishButton);
                td_actions.appendChild(deleteButton);


                tr.appendChild(td_title);
                tr.appendChild(td_description);
                tr.appendChild(td_client_id);
                tr.appendChild(td_client_priority);
                tr.appendChild(td_product_area);
                tr.appendChild(td_target_date);
                tr.appendChild(td_ticket_url);
                tr.appendChild(td_user_id);
                tr.appendChild(td_actions);
                tbody.appendChild(tr);

            });
        }
    });

    $(document).on('click', '.edit', function(event){
        var id = $(this).attr('value');
        window.location = '/editFeature?id=' + id;
    });

});
