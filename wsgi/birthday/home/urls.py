from django.conf.urls import patterns, include, url
from . import views
urlpatterns = [ 
	url(r'^$', views.index),
	url(r'^posts/(?P<username>\w{1,50})/$', views.listPosts),
]
