$(document).ready(function(){
    $('.ui.form').form({
        fields: {
            product_area_name: {
                identifier: 'product_area_name',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter a product area name'
                    },
                    {
                        type: 'minLength[2]',
                        prompt: 'The product area must be more than 2 characters long'
                    }
                ]
            }
        }
    });
});
