from django.conf.urls import patterns, url
from encryption import views

urlpatterns = patterns('',
	url(r'public_key/$', views.display_public_key), 
	url(r'test/$', views.test), 
)
