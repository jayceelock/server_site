"""
This scipt maps the complete URL map of the whole server. It loads the appropriate 
script when a server resource is requested.
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

import views
import register.views
import display_qrcode.views
import user_admin.views
import nfc.views
import nfc_add_user.views
import load_money.views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin', include(admin.site.urls)),
	url(r'^display_qrcode', display_qrcode.views.image),
	url(r'^register', register.views.user_reg),
	url(r'^logout', views.rescan_page),
	url(r'^user_admin', user_admin.views.admin_page),
	url(r'^login', 'django.contrib.auth.views.login'),
	url(r'^nfc', nfc.views.getData),
	url(r'^load_money', load_money.views.load),
	url(r'^add_nfc_user', nfc_add_user.views.add_user),
	url(r'^$', views.main_page),	
)