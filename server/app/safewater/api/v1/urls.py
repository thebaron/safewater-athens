
from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from safewater.api.v1.viewsets import (
    PublicWaterSourceViewSet, ReportViewSet,

    UserViewSet, PermissionViewSet,

)


router = routers.DefaultRouter()

router.register(r'user', UserViewSet)
router.register(r'permissions', PermissionViewSet)

router.register(r'pws', PublicWaterSourceViewSet)
router.register(r'report', ReportViewSet)


pws = PublicWaterSourceViewSet.as_view({
    'get': 'retrieve',
})
pws_list = PublicWaterSourceViewSet.as_view({
    'get': 'list',
})

report = ReportViewSet.as_view({
    'get' : 'retrieve',
})
report_list = ReportViewSet.as_view({
    'get' : 'list'
})



urlpatterns = patterns('api.v1.views',
                       url(r'^pws/by-county/(?P<county>\S+)', pws_list, name='list'),
                       url(r'^pws/(?P<id>[0-9]+)', pws, name='by-id'),
                       url(r'^pws/(?P<pwsid>[A-Z]+[0-9]+)', pws, name='by-pwsid'),
                       url(r'^reports/by-source/(?P<source>\S+)', report_list, name='by-source'),
                       url(r'^reports/by-pwsid/(?P<pwsid>[A-Z]+[0-9]+)', report_list, name='by-pwsid'),
                       url(r'^', include(router.urls)),
                       )
