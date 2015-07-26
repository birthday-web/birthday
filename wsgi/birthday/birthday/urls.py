from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'home.views.err_404'
handler500 = 'home.views.err_500'
urlpatterns = patterns('',
    # Examples:
	url(r'^',include('home.urls')),
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)
