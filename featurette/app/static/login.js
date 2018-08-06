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

      function LoginViewModel() {
          var me = this;
          me.email = ko.observable('');
          me.password = ko.observable('');

          me.buttonEnabled = ko.computed(function() {
              return (me.email() !== "") && (me.password() !== "");
          });

          me.logMeIn = function(){
              $.ajax({
                  url: "api/v1/login",
                  type: "POST",
                  data: { email: me.email(), password: me.password() },
                  success: function (response) {
                      console.log("Response was a success... redirecting to home");
                      window.location.href = "/";
                  }
              });
          }
      }
      ko.applyBindings(new LoginViewModel());

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

      var message = getUrlParameter('message');
      
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

  });
