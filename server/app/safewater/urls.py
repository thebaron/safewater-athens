
from django.conf.urls import patterns, include, url
from django.contrib import admin

from safewater.views import index

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/v1/', include('safewater.api.v1.urls')),

    url(r'^$', index, name='index'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)



