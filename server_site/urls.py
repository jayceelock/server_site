from django.conf.urls import patterns, include, url
from django.contrib import admin
#from encryption.views import generate_key

import views
import register.views
import display_qrcode.views
import user_admin.views
import nfc.views

admin.autodiscover()
#generate_key()

urlpatterns = patterns('',
	url(r'^admin', include(admin.site.urls)),
	url(r'^display_qrcode', display_qrcode.views.image),
	url(r'^register', register.views.user_reg),
	url(r'^logout', views.rescan_page),
	url(r'^user_admin', user_admin.views.admin_page),
	url(r'^login', 'django.contrib.auth.views.login'),
	url(r'^nfc', nfc.views.getData),
	url(r'^$', views.main_page),	
)