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

  });
