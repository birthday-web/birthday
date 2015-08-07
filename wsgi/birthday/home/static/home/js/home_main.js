function confirm(name,pk){
	$(".confirm-box .yes").on("click",function(event){
		event.preventDefault();
		deleteItem(name,pk)
		$(".confirm-box .content").fadeOut("slow",function(){
			$(".confirm-box ").hide();	
		});	
	});
	$(".confirm-box .no").on("click",function(event){
		event.preventDefault();
		$(".confirm-box .content").fadeOut("slow",function(){
			$(".confirm-box ").hide();
		});
	});
	$(".confirm-box ").show(0,function(){
		$(".confirm-box .content").fadeIn("slow");
	});
	
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
    				console.log("success");
    				//remove post/cmt
    				removeItem(name,pk)
    			}else{
    				console.log("failure");
    				//do nothing show error optional
    			}
			},
			error:function(xhr,errmsg,err){
				//do nothing show error optional
			}
		});
	}
}
$(".delete a").each(function(i,item){
	$(this).on("click",function(event){
		event.preventDefault();
		confirm($(this).prop("name"),$(this).data("pk"));
	})
});
