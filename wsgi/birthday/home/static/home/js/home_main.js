function confirm(name,pk){
	$(".confirm-box .yes").on("click",function(event){
		event.preventDefault();
		$(this).off("click");
		console.log($(this));
		if($(this).data('processing')===false){
			$(".confirm-box .yes").data('processing',true);
			deleteItem(name,pk);
			$(".confirm-box .content").fadeOut("slow",function(){
				$(".confirm-box ").hide();
				$(".confirm-box .yes").data('processing',false);
			});
		}
	});
	
	$(".confirm-box .no").on("click",function(event){
		event.preventDefault();
		$(this).off("click");
		$(".confirm-box .content").fadeOut("slow",function(){
			$(".confirm-box ").hide(0,function(){
			});
		});
	});
	$(".confirm-box ").show(0,function(){
		$(".confirm-box .content").fadeIn("slow");
	});
	
}
function addCommentSpinner(button){
	button.html('<i class="fa fa-spinner fa-spin"></i>');
}
function removeCommentSpinner(button){
	button.html('<i class="fa fa-send"></i>');
}

function removeItem(name,pk){
	console.log("removing "+name+" "+pk);
	if(name==="post"){
		$("[name="+name+"][data-pk="+pk+"]").parent().parent().parent().hide("slow",function(){
			$(this).remove();
		});
	}
	else if(name==="cmt"){
		$("[name="+name+"][data-pk="+pk+"]").parent().parent().fadeOut("slow",function(){
			$(this).css({"visibility":"hidden","display":"block"}).slideUp("slow",function(){
			$(this).remove();
			});
		});
	}
}

function deleteItem(name,pk){
	console.log("deleting "+name+" "+pk);
	//delete post ot comment in back
	if(name==="post" || name==='cmt'){
		$.ajax({
			url:'del'+name+'/'+pk,
			type:'GET',
    		success:function(json){
    			console.log(json);
    			if(json['result']){
    				removeItem(name,pk);
    				setNotification(json['msg']);
    			}else{
    				setNotification(json['error']);
    			}
			},
			error:function(xhr,errmsg,err){
				setNotification('Something bad happened, try again!!');
			}
		});
	}
}
function addComment(comment){
	ul=$('#comments-'+comment['post_pk'])
	ul.append('\
		<li>\
			<div class="delete delete-comment" ">\
				<a name="cmt" data-pk="'+comment['comment_pk']+'" href="#" title="Delete this comment"><i class="fa fa-times-circle"></i></a>\
			</div>\
			<a href="/posts/'+comment['author_username']+'" ><h6>'+comment['author_name']+'</h6></a>\
			<p>'+comment['comment']+'</p>\
		</li>\
	');
	li=ul.children().last();
	li.hide();
	li.slideDown('slow',function(){
		$(this).css({'visibility':'visible','display':'block'}).fadeIn(1000);
	});
	setDelete();
}
function createComment(form){
	console.log(form.find('input[type="submit"]'))
	addCommentSpinner(form.find('button[type="submit"]'));
	var csrftoken=getCookie('csrftoken');
	$.ajax({
		url:'./create_comment/',
		data:form.serialize(),
		method:"POST",
		beforeSend: function(xhr, settings) {
			$("#logout-button").html("Signout <i class=\"fa fa-spinner fa-spin\"></i>");
        	if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        	    xhr.setRequestHeader("X-CSRFToken", csrftoken);
        	}
    	},
		success:function(json){
			if(json['status']){
				setNotification(json['msg'],false);
				addComment(json['comment']);
				form[0].reset();
			}
			else{
				setNotification(json['error'],false);
			}
			removeCommentSpinner(form.find('button[type="submit"]'));
			form.data('processing',false);
		},
		error:function(xhr,errmsg,err){
			console.log(xhr);
			removeCommentSpinner(form.find('button[type="submit"]'));
			form.data('processing',false);
		}
	});
}
function clearPostFormErrors(){
	$('.post-form-errors').each(function(i,ul){
		$(this).empty();
	})
}
function addPost(post){
	var posts=$('#posts-section-container')
	posts.append('\
		<div class="col-sm-4">\
					<div class="thumbnail">\
						<div class="delete delete-post" >\
							<a name="post" data-pk="'+post['post_pk']+'" href="#" title="Delete this post"><i class="fa fa-times-circle"></i></a>\
						</div>\
						<img src="'+post['image']+'"/>\
						<div class="caption">\
						'+post['caption']+'\
							<hr>\
							Author - <a href="/posts/'+post['author_username']+'">'+post['author_name']+'</a>\
							<hr>\
								<div>\
									<ul id="comments-'+post['post_pk']+'" class="comments">\
									</ul>\
								</div>\
								<form data-processing="false" class="comment-form" action="." method="post">\
									<input type="hidden" name="csrfmiddlewaretoken" value="'+getCookie("csrftoken")+'" />\
										<div class="form-group">\
											<input class="form-control" id="id_comment" maxlength="200" name="comment" placeholder="Comment" type="text" required />\
										</div>\
									<input id="id_post" name="post" type="hidden" value="'+post['post_pk']+'">\
									<div class="form-group">\
										<button class="btn btn-primary" name="comment_button" type="submit"><i class="fa fa-send"></i></button>\
									</div>\
								</form>\
						</div>\
					</div>\
				</div>\
	');
	var new_post=posts.children().last();
	new_post.hide();
	new_post.show('slow');
	setComment();
	setDelete();
}
function createPost(form){
	clearPostFormErrors();
	addSpinner(form.find('button[name="post_button"]'));
	var formData=new FormData($('#post-form')[0])
	$.ajax({
		url:'./create_post/',
		type:"POST",
		data:formData,
		cache: false,
		contentType: false,
		processData: false,
		success:function(json){
			if(json['status']){
				setNotification(json['msg'],false);
				$('#post-form')[0].reset();
				addPost(json['post']);
			}
			else{
				setNotification(json['error'],false);
				if(json['errors']){
					console.log(json['errors']);
					$.each(json['errors'],function(field,errors){
						ul=$('#post-'+field);
						$.each(errors,function(index,error){
							ul.append('\
							<li><i class="fa fa-asterisk"></i> '+error+'</li>\
							');
						});
					});
				}
			}
			form.data('processing',false);
			removeSpinner($('button[name="post_button"]'));
			
		},
		error:function(xhr,errmsg,err){
			setNotification('something went wrong, try again !!',false);
			console.log(xhr);
			removeSpinner($('button[name="post_button"]'));
			form.data('processing',false);
		}
	});
}
function setDelete(){
	$(".delete a").each(function(i,item){
		$(this).off("click");
		$(this).on("click",function(event){
			event.preventDefault();
			confirm($(this).prop("name"),$(this).data("pk"));
		})
	});
}
function setComment(){
	$('.comment-form').each(function(){
		$(this).off('submit');
		$(this).on('submit',function(event){
			event.preventDefault();
			if($(this).data('processing')===false){
				$(this).data('processing',true);
				createComment($(this));
			}
			else{
				setNotification('wait for previous action to complete',false);
			}
		});
	});
}
function setPost(){
	$('#post-form').off('submit');
	$('#post-form').on('submit',function(event){
	event.preventDefault();
	if($(this).data('processing')===false){
		$(this).data('processing',true);
		createPost($(this));
	}else{
		setNotification('wait for previous action to complete',false);
	}
	});
}
setDelete();
setComment();
setPost();

