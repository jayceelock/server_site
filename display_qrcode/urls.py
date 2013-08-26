from django.conf.urls import patterns, url
from display_qrcode import qrcode

urlpatterns = patterns('',
	url(r'^', qrcode.image), 
)
