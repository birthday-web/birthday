from django.conf.urls import patterns, include, url
from . import views
from django.conf.urls import handler404, handler500

handler404 = views.index

urlpatterns = [ 
	url(r'^$', views.index),
	url(r'^login/$', views.do_login),
	url(r'^logout/$', views.do_logout),
	url(r'^posts/(?P<username>[-\w.]+)/$', views.listPosts),
	url(r'^posts/(?P<username>[-\w.]+)/delcmt/(?P<comment_id>\d){1,10}/$', views.delComment),
	url(r'^posts/(?P<username>[-\w.]+)/delpost/(?P<post_id>\d{1,10})/$', views.delPost),
]
