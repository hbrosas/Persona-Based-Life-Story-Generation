
//Facebook SDK
$(document).ready(function() {
    console.log('Testing');
    window.fbAsyncInit = function() {
        FB.init({
            appId      : '139479073449755',
            cookie     : true,
            autoLogAppEvents : true,
            xfbml      : true,
            version    : 'v3.0'
        });

        FB.AppEvents.logPageView();
    };

    (function(d, s, id){
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) {return;}
        js = d.createElement(s); js.id = id;
        js.src = "https://connect.facebook.net/en_US/sdk.js";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
});


//Facebook Graph API
$(document).on("click", "#loginFB", function() {
    FB.login(function(response) {
        if (response.authResponse) {
            console.log('Yoooo Welcome!  Fetching your information for TESTING.... ');
            var accessToken = response.authResponse.accessToken;
            sessionStorage.setItem("fbResponse", response);
            window.location.href = "http://localhost:8000/loading/";
//            console.log("Access Token: " + accessToken);

            FB.api('/me', function(response) {
                console.log('Good to see you, ' + response.name + "!!!!!!!!!");
                //Get Personal Info, Posts, Likes, Events for Testing
                FB.api(
                    '/me',
                    'GET',
                    // DEPRACATED: {"fields":"id,name,gender,birthday,address,location,hometown,about,friends,education,work,posts.limit(5000){story,description,message,updated_time},likes.limit(5000){name,category,about,description},events.limit(5000){name,description,rsvp_status}"},
                    {"fields":"id,name,gender,birthday,address,location,hometown,friends,posts.limit(5000){story,description,message,updated_time},likes.limit(5000){name,category,about,description},events.limit(5000){name,description,rsvp_status}"},
                    getPersonalInfo
                )
            });

        } else {
            console.log('User cancelled login or did not fully authorize.');
        }
    }, {
        scope: 'user_birthday, user_friends, user_hometown, user_likes, user_location, user_posts,user_likes,user_events',
        auth_type: 'rerequest',
        return_scopes: true
    });
});

