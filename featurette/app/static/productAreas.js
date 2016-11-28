$(document).ready(function(){
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

    $.getJSON({
        url: 'http://localhost:5000/api/v1/productAreas',
        dataType: 'json',
        success: function(data){
            $.each(data, function(index, element) {
                //getting the table body
                var tbody = document.getElementById('productAreasTable');

                //td information
                var tr = document.createElement('tr');
                var td = document.createElement('td');
                td.textContent= element.name;

                //td actions
                var td_actions = document.createElement('td');
                td_actions.setAttribute('class', 'single line');

                var form = document.createElement('form');+
                form.setAttribute('action', '/editProductArea');
                form.setAttribute('method', 'GET');

                var editButton = document.createElement('a');
                editButton.setAttribute('class', 'edit ui icon violet button');
                editButton.setAttribute('value', element.id);
                editButton.setAttribute('href', '/editProductArea');

                var editIcon = document.createElement('i');
                editIcon.setAttribute('class', 'edit icon');
                editButton.appendChild(editIcon);
                form.appendChild(editButton);

                var deleteButton = document.createElement('a');
                deleteButton.setAttribute('class', 'delete ui icon red button');
                deleteButton.setAttribute('value', element.id);

                var deleteIcon = document.createElement('i');
                deleteIcon.setAttribute('class', 'delete icon');
                deleteButton.appendChild(deleteIcon);

                td_actions.appendChild(form);
                td_actions.appendChild(deleteButton);


                tr.appendChild(td);
                tr.appendChild(td_actions);
                tbody.appendChild(tr);

            });
        }
    });
});
