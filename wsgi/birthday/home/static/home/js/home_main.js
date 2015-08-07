function removeItem(name,pk){
	console.log("removing "+name+" "+pk);
	if(name==="post"){
		$("[name="+name+"][data-pk="+pk+"]").parent().parent().parent().hide("slow",function(){
			$(this).remove();
		});
	}
	else if(name==="cmt"){
		$("[name="+name+"][data-pk="+pk+"]").parent().parent().hide("slow",function(){
			$(this).remove();
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
		$name=$(this).prop("name");
		deleteItem($name,$(this).data("pk"));
	})
});
