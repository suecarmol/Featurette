$(document).ready(function(){
    $('.ui.form').form({
        fields: {
            username: {
                identifier: 'username',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter a username'
                    },
                    {
                        type: 'minLength[6]',
                        prompt: 'Username must have at least 6 characters'
                    }
                ]
            },
            email: {
                identifier: 'email',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter an email'
                    },
                    {
                        type: 'email',
                        prompt: 'Email must ve a valid email'
                    }
                ]
            },
            password: {
                identifier: 'password',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter a password'
                    },
                    {
                        type: 'minLength[8]',
                        prompt: 'Password must have at least 8 characters'
                    }

                ]
            }
        }
    });
});
