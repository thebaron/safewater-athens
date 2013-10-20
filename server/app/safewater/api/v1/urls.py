
from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from safewater.api.v1.viewsets import (
    PublicWaterSourceViewSet, ReportViewSet, ActionViewSet,

    UserViewSet, PermissionViewSet,

)


router = routers.DefaultRouter()

router.register(r'user', UserViewSet)
router.register(r'permissions', PermissionViewSet)

router.register(r'pws', PublicWaterSourceViewSet)
router.register(r'report', ReportViewSet)
router.register(r'action', ActionViewSet)


pws_detail = PublicWaterSourceViewSet.as_view({
    'get': 'retrieve',
})
pws_list = PublicWaterSourceViewSet.as_view({
    'get': 'list',
})

report_detail = ReportViewSet.as_view({
    'get' : 'retrieve',
})
report_list = ReportViewSet.as_view({
    'get' : 'list'
})

action_detail = ActionViewSet.as_view({
    'get' : 'retrieve',
})
action_list = ActionViewSet.as_view({
    'get' : 'list'
})




urlpatterns = patterns('api.v1.views',
                       url(r'^pws/by-county/(?P<county>\S+)', pws_list, name='pws-list'),
                       url(r'^pws/(?P<pk>[0-9]+)', pws_detail, name='pws-detail'),
                       url(r'^pws/(?P<pwsid>[A-Z]+[0-9]+)', pws_detail, name='pws-detail'),

                       url(r'^report/(?P<pk>[0-9]+)', report_detail, name='report-detail'),

                       url(r'^action/(?P<pk>[0-9]+)', action_detail, name='action-detail'),

                       # url(r'^reports/by-source/(?P<source>\S+)', report_list, name='by-source'),
                       # url(r'^reports/by-pwsid/(?P<pwsid>[A-Z]+[0-9]+)', report_list, name='by-pwsid'),
                       url(r'^', include(router.urls)),
                       )
