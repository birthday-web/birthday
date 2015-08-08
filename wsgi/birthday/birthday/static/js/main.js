notification_timer=''
spinner='<i class="fa fa-spinner fa-spin notification-spinner"></i>';
function setNotification(msg,reload){
	$('.notification-spinner').remove();
	$('#notification-panel').html(msg+(reload?' '+spinner:'')+'<br>'+$('#notification-panel').html());
	$('#notification-panel').fadeIn('slow');
	clearTimeout(notification_timer);
	notification_timer=setTimeout(function(){
		$('#notification-panel').fadeOut('slow',function(){
			$('#notification-panel').html('');
			if(reload){
				location.reload(true);
			}
		});
		
	},(reload?1000:3000));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function remove_register_div(){
	register_div.fadeOut(1000,function(){
		$(this).css({"visibility":"hidden","display":'block'}).slideUp();
	});
}

function add_register_div(){
	register_div.slideDown("slow",function(){
		$(this).css({"visibility":"visible","display":'block'}).fadeIn(1000);
	});
}

/*
*	update all CSRF token so that next request does not crash
*/
function updateCsrf(){
	var csrftoken=getCookie('csrftoken');
	$('[name="csrfmiddlewaretoken"]').each(function(i,item){
		$(this).val(csrftoken);
	});
}

/*
* add a loading sppiner to the button (any DOM element will do)
*/
function addSpinner(button){
	button.html(button.html()+' <i class="fa fa-spinner fa-spin"></i>');
}

/*
* remove the spinner if any
*/
function removeSpinner(button){
	button.children('.fa-spin').remove()
}

//login logout

/*login_msg_timer=''
function setLoginMsg(msg,success,main){
	if(main){
		login_msg=$('#login-msg-main');
	}else{
		login_msg=$('#login-msg');
	}
	console.log("setting msg");
	if(success){
		login_msg.html('<div class="alert alert-success">'+msg+'</div>');
		login_msg.slideDown("slow",function(){
			$(this).css({"visibility":"visible","display":'block'}).fadeIn(1000);
		});
		clearTimeout(login_msg_timer);
		login_msg_timer=setTimeout(function(){
			location.reload(true);
		},1000);
		
	}else{
		login_msg.html('<div class="alert alert-danger">'+msg+'</div>');
		login_msg.slideDown("slow",function(){
			$(this).css({"visibility":"visible","display":'block'}).fadeIn(1000);
		});
		clearTimeout(login_msg_timer);
		login_msg_timer=setTimeout(function(){
			login_msg.fadeOut(500,function(){
				$(this).css({"visibility":"hidden","display":'block'}).slideUp();
			});
		},4000);
	}
}
*/
function setLogout(){
	$('#logout-form').on('submit',function(event){
		event.preventDefault();
		doLogout();
	});
}
function doLogout(){
	var csrftoken=getCookie('csrftoken');
	console.log("log out request");
	$.ajax({
		url:'/logout/',
		type:'POST',
		cache:false,
		data:$('#logout-form').serialize(),
		beforeSend: function(xhr, settings) {
			$("#logout-button").html("Signout <i class=\"fa fa-spinner fa-spin\"></i>");
        	if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        	    xhr.setRequestHeader("X-CSRFToken", csrftoken);
        	}
    	},
    	success:function(json){
    		console.log("logout");
    		if(json['status']){
	    		setNotification(json['msg'],true);
    			$('#before-login').hide();
    			$('#before-login').html('\
    				<h4 class="heading">Login </h4>\
				<form id="login-form" action="/login/" method="post" class="sidebar-form"><input type="hidden" name="csrfmiddlewaretoken" value=" " />\
						<div class="form-group">\
							<input class="form-control" id="id_username" maxlength="30" name="username" placeholder="Username" type="text" required />\
							<ul id="username_error" class="errorlist"></ul>\
						</div>\
						<div class="form-group">\
							<input Placeholder="Password" class="form-control" id="id_password" maxlength="128" name="password" type="password" />\
							<ul id="password_error" class="errorlist"></ul>\
						</div>\
					<div class="form-group">\
						<button id="login-button" name="login_button" class="btn btn-primary" type="Submit" >Signin</button>\
					</div>\
				</form>\
    			');
    			$('#after-login').fadeOut(500,function(){
    				$('#before-login').fadeIn(500);
    			});
       		}
    		add_register_div();
    		updateCsrf();
    		setLogin();
    	},
    	error:function(xhr,errmsg,err){
    		console.log("error logout");
    	}
});
}
function setLogin(){
	$('#login-form').on('submit',function(event){
		event.preventDefault();
		doLogin(false);
	});
	$('#login-form-main').on('submit',function(event){
		event.preventDefault();
		doLogin(true);
	});
}

function doLogin(main){
	if(main){
		login_form=$('#login-form-main');
		login_button=$('#login-button-main');
	}
	else{
		login_form=$('#login-form');
		login_button=$('#login-button');
	}

	addSpinner(login_button);
	var csrftoken=getCookie('csrftoken');
	$('.errorlist').each(function(i,ul){
		$(this).empty();
	});
	$.ajax({
		url:'/login/',
		type:'POST',
		data:login_form.serialize(),
		cache:false,
		beforeSend: function(xhr, settings) {
        	if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        	    xhr.setRequestHeader("X-CSRFToken", csrftoken);
        	}
    	},
    	success:function(json){
    		if(json['status']){
	   			setNotification(json['msg'],true);
    			$('#after-login').hide();
    			$('#after-login').html('\
    				<div class="thumbnail">\
					<img src="'+json['image_url']+'">\
				</div>\
				<h4 class="heading">'+json['full_name']+'</h4>\
				<p>\
					<strong class="heading">Username</strong><br>'+json['username']+'<br>\
					<strong class="heading">Email</strong><br>'+json['email']+'<br>\
					<strong class="heading">Date of Birth</strong><br>'+json['date_of_birth']+'<br>\
					<strong class="heading">Number of Posts</strong><br>'+json['post_count']+'<br>\
				</p>\
				<form id="logout-form" class="sidebar-form" method="post" >\
				'+csrf_input+'\
					<button id="logout-button" name="logout_button" class="btn btn-primary" type="Submit" >Signout</button>\
				</form>\
    			');
    			$('#before-login').fadeOut(500,function(){
    				$('#after-login').fadeIn(500);
    			});
    			setLogout();
    			remove_register_div();
    			
    		}
    		else{
    			setNotification(json['error'],false);
    		}
    		updateCsrf();
    		removeSpinner(login_button);
    	},
    	error: function(xhr,errmsg,err){
    		setNotification('Login attempt failed',false);
			removeSpinner(login_button);
    	}
	});
	
}

//adding new friend
/*
add_friend_msg_timer=''
function setAddFriendMsg(msg,success){
	$('#add-friend-msg').html('<div class="alert alert-'+(success?'success':'danger')+'">'+msg+'</div>');
	$('#add-friend-msg').slideDown("slow",function(){
			$(this).css({"visibility":"visible","display":'block'}).fadeIn(1000);
	});
	clearTimeout(add_friend_msg_timer);
	add_friend_msg_timer=setTimeout(function(){
			$('#add-friend-msg').fadeOut(500,function(){
				$(this).css({"visibility":"hidden","display":'block'}).slideUp();
			});
		},4000);
}
*/
function setAddFriend(){
	$("#add-friend-form").on('submit',function(event){
		event.preventDefault();
		AddFriend();
	})
}
function AddFriend(){
	form=$('#add-friend-form');
	submit_button=$('#add-friend-submit-button');
	addSpinner(submit_button);
	$.ajax({
		url:'/add_friend_request/',
		data:form.serialize(),
		type:"POST",
		success:function(json){
			if(json['result']){
				setNotification(json['msg'],false);
			}
			else{
				setNotification(json['error'],false);
			}
			removeSpinner(submit_button);
		},
		error:function(xhr,errmsg,err){
			console.log(err);
			removeSpinner(submit_button);
		},
	});
}

//accept reject friend requests
function setAcceptRequest(){
	$(".accept-request").each(function(){
		$(this).on('click',function(event){
			event.preventDefault();
			processRequest(true,$(this).data("pk"));
		});
	});
}
function setRejectRequest(){
	$(".reject-request").each(function(){
		$(this).on('click',function(event){
			event.preventDefault();
			processRequest(false,$(this).data("pk"));
		});
	});
}
function refreshFriendRequestList(request_id){
	$('#request-'+request_id).hide('slow',function(){
		$(this).remove();
		if($('#friend-request-list li').length > 0)
			console.log("stay");
		else{
			$('#friend-request-section').hide('slow',function(){
				$(this).remove();
			});
		}
	});
}
function refreshFriendList(primary_friends,friends){
	console.log("reset friend list"+primary_friends.length+" "+friends.length);
	$('#primary-friend-row').hide('slow');
	$('#primary-friend-row').empty();
	$.each(primary_friends,function(key,pf){
		var new_div='\
			<div class="col-sm-4 col-sm-offset-4" >\
						<div class="thumbnail">\
							<img src="'+pf['image']+'">\
							<div class="caption">\
								<h4>'+pf['name']+'<br><small>'+pf['dob']+'</small></h4>\
								<a class="btn btn-primary" href="posts/'+pf['username']+'"><i class="fa fa-birthday-cake"></i></a>\
							</div>\
							</img>\
						</div>\
					</div>\
		';
		$('#primary-friend-row').append(new_div);
	});
	$('#primary-friend-row').show('slow');

	$('#friend-row').hide('slow');
	$('#friend-row').empty();
	$.each(friends,function(key,pf){
		new_div='\
			<div class="col-xs-6 col-sm-3">\
				<div class="thumbnail">\
					<img src="'+pf['image']+'">\
					<div class="caption">\
						<h4>'+pf['name']+'<br><small>'+pf['dob']+'</small></h4>\
						<a class="btn btn-primary" href="posts/'+pf['username']+'"><i class="fa fa-birthday-cake"></i></a>\
					</div>\
				</div>\
			</div>\
		';
		//$(new_div).hide().appendTo('#friend-row').fadeIn();
		$('#friend-row').append(new_div);
	});
		$('#friend-row').show('slow');
}
function processRequest(accept,request_id){
	$.ajax({
		url:'/request_'+(accept?'accept':'reject')+'/'+request_id,
		type:"GET",
		success:function(json){
			console.log(json);
			if(json['status']){
				setNotification(json['msg']);
				refreshFriendRequestList(request_id);
				//add firend to existing list
				refreshFriendList(json['primary_friends'],json['friends']);
			}
			else{
				setNotification(json['error']);
			}
		},
		error:function(xhr,errmsg,err){
			console.log(errmsg);
		}
	});
}
//initial setup calls

setAddFriend();
setLogin();
setLogout();
register_div=$('#get_listed');
setAcceptRequest()
setRejectRequest()
$('#notification-panel').hide();

$(window).load(function(){
  $(".js-toggle-sidebar").on('click', function() {
	$(".navbar").toggleClass("js-navbar-aside");
	 $(".wrapper").toggleClass("js-wrapper-aside");
    $(".sidebar").toggleClass("js-sidebar-aside");
    $(".footer").toggleClass("js-footer-aside");
    return false;
});
});

$(window).scroll(function(){
    if($(this).scrollTop() > 50)
    {   
        $(".navbar").addClass('navbar-inverse');
        $(".header").addClass('header-inverse');
    }else{
		$(".navbar").removeClass('navbar-inverse');
		$(".header").removeClass('header-inverse');
	}
});

