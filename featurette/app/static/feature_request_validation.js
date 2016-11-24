$( document ).ready(function() {

    $('.ui.form').form({
        fields: {
            request_title: {
                identifier: 'request_title',
                rules: [
                    {
                        type   : 'empty',
                        prompt : 'Please enter the title of the feature request'
                    }
                ]
            },
            request_description: {
                identifier: 'request_description',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter the description of the feature request'
                    },
                    {
                        type: 'minLength[10]',
                        prompt: 'Your description has to have at least 10 characters'
                    }
                ]
            },
            client_priority: {
                identifier: 'client_priority',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter a priority'
                    },
                    {
                        type: 'integer[1..100000000]',
                        prompt: 'Number must be a positive integer'
                    }
                ]
            },
            target_date: {
                identifier: 'target_date',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter a date'
                    }
                ]
            },
            ticket_url: {
                identifier: 'ticket_url',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter a URL'
                    },
                    {
                        type: 'url',
                        prompt: 'The content must be a valid URL'
                    }
                ]
            },
            client: {
                identifier: 'client',
                rules: [
                    {
                        type:'empty',
                        prompt: 'Please select a client'
                    }
                ]
            },
            product_area: {
                identifier: 'product_area',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please select a product area'
                    }
                ]
            }
        }
    });
});
