$(document).ready(function() {
    $('.ui.form')
      .form({
        fields: {
          email: {
            identifier  : 'email',
            rules: [
              {
                type   : 'empty',
                prompt : 'Please enter your e-mail'
              },
              {
                type   : 'email',
                prompt : 'Please enter a valid e-mail'
              }
            ]
          },
          password: {
            identifier  : 'password',
            rules: [
              {
                type   : 'empty',
                prompt : 'Please enter your password'
              },
              {
                type   : 'minLength[8]',
                prompt : 'Your password must be at least 8 characters'
              }
            ]
          }
        }
      });

      $('.message .close').on('click', function() {
          $(this).closest('.message').transition('fade');
      });

      //logging user in
      $('#login').click(function(){
          var email = $('#email').val();
          var password = $('#password').val();
          $.ajax({
              url: 'http://localhost:5000/api/v1/login',
              type: 'POST',
              data: {email : email, password: password},
              success: function(data){
                  console.log('Login was successful');
              },
              error: function(xhr,err){
                  console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
                  console.log("responseText: "+xhr.responseText);
              }
          });
  	});

  });
