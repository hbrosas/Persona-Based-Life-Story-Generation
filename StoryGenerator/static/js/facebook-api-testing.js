
//Facebook SDK
$(document).ready(function() {
    console.log('Testing');
    window.fbAsyncInit = function() {
        FB.init({
            appId      : '139479073449755',
            cookie     : true,
            xfbml      : true,
            version    : 'v2.11'
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
//            console.log("Access Token: " + accessToken);

            FB.api('/me', function(response) {
                console.log('Good to see you, ' + response.name + "!!!!!!!!!");
			    //window.location.href = "http://localhost:8000/loading/";

             //Get Personal Info, Posts, Likes, Events for Testing
                FB.api(
                    '/me',
                    'GET',
                    {"fields":"id,name,gender,birthday,address,location,hometown,about,friends,education,work,posts.limit(5000){story,description,message,updated_time},likes.limit(5000){name,category,about,description},events.limit(5000){name,description,rsvp_status}"},
                    getPersonalInfo
                )
            });

        } else {
            console.log('User cancelled login or did not fully authorize.');
        }
    }, {
        scope: 'user_about_me, user_birthday, user_education_history, user_friends, user_hometown, user_likes, user_location, user_work_history, user_posts,user_likes,user_events',
        auth_type: 'rerequest',
        return_scopes: true
    });

    var i = 0, j = 0, k = 0, l = 0;
    var pString = "", lString = "", eString = "";

    var personalInfo = {};
    var education, work;
    var posts = [];
    var likes = [];
    var events = [];
    var pFlag = false, lFlag = false, eFlag = false;

    function getPersonalInfo(response){

        var location = null;
        var hometown = null;

        if(response.location != null || response.hometown != null){
            location = response.location.name
        }else{
            hometown = response.hometown.name
        }

        personalInfo = {
                'id': response.id,
                'name': response.name,
                'gender':  response.gender,
                'birthday': response.birthday,
                'address': response.address,
                'location': location,
                'hometown': hometown,
                'about': response.about,
                'friends': response.friends.summary.total_count,
                'education': response.education,
                'work': response.work,
                }

        console.log("education", response.education);
        console.log("work", response.work);

        education = response.education;
        work = response.work;
//        education.push(JSON.stringify(response.education));
//        work.push(JSON.stringify(response.work));


        console.log("id:", personalInfo['id']);
        console.log("name: ", personalInfo['name']);
        console.log("gender", personalInfo['gender']);
        console.log("birthday", personalInfo['birthday']);
        console.log("address", personalInfo['address']);
        console.log("location", personalInfo['location']);
        console.log("hometown", personalInfo['hometown']);
        console.log("about", personalInfo['about']);
        console.log("friends", personalInfo['friends']);


        getPosts(response);

    }

    function getPosts(response){
        origresponse = response;
        console.log("POSTS");
        pString += JSON.stringify(response.posts.data).substring(0, JSON.stringify(response.posts.data).length - 1);
        if (response.posts.paging != undefined) {
            nextPage = response.posts.paging.next;
            $.get(nextPage, postsIterate = function(response) {
                if (JSON.stringify(response.data) != "[]"){
                    var temp = JSON.stringify(response.data).substring(1, JSON.stringify(response.data).length - 1);
					pString += "," + temp;

					if (response.paging.next != undefined){
                        console.log("j " + j)
						nextPage = response.paging.next;
						j++;
						$.get(nextPage, postsIterate, "json");

					}else if (response.paging == undefined) {
					    pString += "]";
						posts.push(JSON.parse(pString));
						pFlag = true;
						console.log(posts);
						getLikes(origresponse);
					}
                }else {
				    pString += "]";
					posts.push(JSON.parse(pString));
					pFlag = true;
					console.log(posts);
					getLikes(origresponse);
				}
            }, "json");
        } else {
		    pString += "]";
			posts.push(JSON.parse(pString));
			pFlag = true;
			console.log(likes);
			getLikes(origresponse);
		}
    } //end of function of getPosts


    function getLikes(response){
        origresponse = response;
        console.log("LIKES");
        lString += JSON.stringify(response.likes.data).substring(0, JSON.stringify(response.likes.data).length - 1);
        if (response.likes.paging != undefined) {
            nextPage = response.likes.paging.next;
            $.get(nextPage, likesIterate = function(response) {
					if (JSON.stringify(response.data) != "[]"){
						var temp = JSON.stringify(response.data).substring(1, JSON.stringify(response.data).length - 1);
						lString += "," + temp;
						if (response.paging.next != undefined) {
						    console.log("l " + l)
							nextPage = response.paging.next;
							l++;
							$.get(nextPage, likesIterate, "json");
						} else {
							lString += "]";
							likes.push(JSON.parse(lString));
		 					lFlag = true;
		 					console.log(likes);
		 					getEvents(origresponse);
		 				}
					} else {
						lString += "]";
						likes.push(JSON.parse(lString));
						lFlag = true;
						console.log(likes);
						getEvents(origresponse);
					}
            }, "json");

        }else {
		    lString += "]";
			likes.push(JSON.parse(lString));
			lFlag = true;
			console.log(likes);
			getEvents(origresponse);
	    }

    } // end of function getLikes

    function getEvents(response){
        origresponse = response;
		console.log("EVENTS");
		eString += JSON.stringify(response.events.data).substring(0, JSON.stringify(response.events.data).length - 1);
        if (response.events.paging.next != undefined){
            nextPage = response.events.paging.next;
            $.get(nextPage, eventsIterate = function(response) {
                if (JSON.stringify(response.data) != "[]"){
                    var temp = JSON.stringify(response.data).substring(1, JSON.stringify(response.data).length - 1);
                    eString += "," + temp;
                    if (response.paging.next != undefined) {
                        console.log("k " + k)
						nextPage = response.paging.next;
						console.log("inside events nextPage " + nextPage)
						k++;
						$.get(nextPage, eventsIterate, "json");
                    }else {
					    eString += "]";
						events.push(JSON.parse(eString));
			 			eFlag = true;
			 			console.log(events);
			 			storeToDb();
			 		}
                }else {
				    eString += "]";
					events.push(JSON.parse(eString));
					eFlag = true;
					console.log(events);
					storeToDb();
				}
            }, "json");
        }else {
		    eString += "]";
			events.push(JSON.parse(eString));
			eFlag = true;
			console.log(events);
            storeToDb();
	    }

    } // end of function getEvents

    //Execute facebookgraphapi.py
    function storeToDb(){
        console.log("Store to DB!!!");
        console.log(personalInfo);
        $.ajax({
            url: '/ajax/store_testing_data/',
            type : "POST",
            data: {
              'personalInfo': JSON.stringify(personalInfo),
              'education': JSON.stringify(education),
              'work': JSON.stringify(work),
              'posts': JSON.stringify(posts),
              'likes': JSON.stringify(likes),
              'events': JSON.stringify(events)
            },
            dataType: 'json',
            success: function (data) {
                alert("Profile, Education & Work Background, posts, likes, and events successfully extracted. Thank you!");
            }
        });
    }

});

