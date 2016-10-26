$(document).ready(function(){
    $('.ui.form').form({
        fields: {
            client_name: {
                identifier: 'client_name',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter a client'
                    }
                ]
            }
        }
    })
});
