
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

function setLogin(){
	$('#login-form').on('submit',function(event){
		event.preventDefault();
		doLogin();
	});
}
setLogin();
function setLogout(){
	$('#logout-form').on('submit',function(event){
		event.preventDefault();
		doLogout();
	});
}
setLogout();
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
register_div=$('#get_listed');

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
function updateCsrf(){
	var csrftoken=getCookie('csrftoken');
	$('[name="csrfmiddlewaretoken"]').each(function(i,item){
		$(this).val(csrftoken);
	});
}
timer="";
function setLoginMsg(msg,success){
	if(success){
		$('#login-msg').html('<div class="alert alert-success">'+msg+'</div>');
		$('#login-msg').slideDown("slow",function(){
			$(this).css({"visibility":"visible","display":'block'}).fadeIn(1000);
		});
		clearTimeout(timer);
		timer=setTimeout(function(){
			location.reload(true);
			/*$('#login-msg').fadeOut(500,function(){
				$(this).css({"visibility":"hidden","display":'block'}).slideUp();
				
			});*/
		},1000);
		
	}else{
		$('#login-msg').html('<div class="alert alert-danger">'+msg+'</div>');
		$('#login-msg').slideDown("slow",function(){
			$(this).css({"visibility":"visible","display":'block'}).fadeIn(1000);
		});
		clearTimeout(timer);
		timer=setTimeout(function(){
			$('#login-msg').fadeOut(500,function(){
				$(this).css({"visibility":"hidden","display":'block'}).slideUp();
			});
		},2000);
	}
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
			$("#logout-button").html("Signout <i class=\"fa fa-spinner fa-pulse\"></i>");
        	if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        	    xhr.setRequestHeader("X-CSRFToken", csrftoken);
        	}
    	},
    	success:function(json){
    		console.log("logout");
    		if(json['success']){
	    		setLoginMsg('Succeessfully Sign out',true);
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
						<input id="login-button" name="login_button" class="btn btn-primary" type="Submit" value="Sign in"/>\
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
function doLogin(){
	var csrftoken=getCookie('csrftoken');
	$('.errorlist').each(function(i,ul){
		$(this).empty();
	});
	
	$.ajax({
		url:'/login/',
		type:'POST',
		data:$('#login-form').serialize(),
		cache:false,
		beforeSend: function(xhr, settings) {
			$("#login-button").html("Signin <i class=\"fa fa-spinner fa-pulse\"></i>");
        	if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        	    xhr.setRequestHeader("X-CSRFToken", csrftoken);
        	}
    	},
    	success:function(json){
    		console.log("success");
    		if(json['success']){
    		//show message done
    		//hide login form done
    		//show data done
    		//hide register form
    		setLoginMsg('Login succeessful',true)
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
					<input id="logout-button" name="logout_button" class="btn btn-primary" type="Submit" value="Sign out">\
				</form>\
    			');
    			$('#before-login').fadeOut(500,function(){
    				$('#after-login').fadeIn(500);
    			});
    			setLogout();
    			remove_register_div();
    		}
    		else if(json['error']){
    			setLoginMsg('Login attempt failed',false);
    		}
    		updateCsrf();
    	},
    	error: function(xhr,errmsg,err){
    		setLoginMsg('Login attempt failed',false);
    	}
	});
	
}



