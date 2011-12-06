from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from gimmebar.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', landing),
	(r'^gimmeauth/$', authenticate),
	(r'^exchange/$', exchange),
	(r'^graphs/$', graphs),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    url(r'^admin/', include(admin.site.urls)),
)
