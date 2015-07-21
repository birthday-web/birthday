
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

