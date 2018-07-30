$(document).ready(function() {
    function LogoutViewModel() {
        var me = this;
        me.logMeOut = function(){
            $.ajax({
                url: "api/v1/logout",
                type: "POST",
                success: function (response) {
                    console.log("Log out was a success... redirecting to login");
                    window.location.href = "/login";
                }
            });
        }
    }
    ko.applyBindings(new LogoutViewModel());
});
