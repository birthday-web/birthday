from django.conf.urls import patterns, include, url
from . import views
from django.conf.urls import handler404, handler500

handler404 = views.index

urlpatterns = [ 
	url(r'^$', views.index),
	url(r'^login/$', views.do_login),
	url(r'^logout/$', views.do_logout),
	url(r'^add_friend_request/$', views.add_friend_request),
	url(r'^request_accept/(?P<request_id>\d+)/$', views.acceptRequest),
	url(r'^request_reject/(?P<request_id>\d+)/$', views.rejectRequest),
	url(r'^registration/$', views.register),
	url(r'^posts/(?P<username>[-\w.]+)/$', views.listPosts),
	url(r'^posts/(?P<username>[-\w.]+)/create_post/$', views.createPost),
	url(r'^posts/(?P<username>[-\w.]+)/delpost/(?P<post_id>\d+)/$', views.delPost),
	url(r'^posts/(?P<username>[-\w.]+)/create_comment/$', views.createComment),	
	url(r'^posts/(?P<username>[-\w.]+)/delcmt/(?P<comment_id>\d+)/$', views.delComment),

]
