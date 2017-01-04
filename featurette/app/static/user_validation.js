$(document).ready(function(){
    $('.ui.form').form({
        fields: {
            username: {
                identifier: 'username',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter a username'
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
            },
            repeat_password: {
                identifier: 'repeat_password',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please re-enter your password'
                    },
                    {
                        type: 'match[password]',
                        prompt: 'The passwords do not match'
                    }
                ]
            }
        }
    });
});
