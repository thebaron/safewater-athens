
from django.contrib.auth.models import User, Permission
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.permissions import AllowAny

from safewater.api.renderers import HALJSONRenderer, PDFRenderer
from safewater.models import PublicWaterSource, Report

# Django Models

class UserViewSet(viewsets.ModelViewSet):
    model = User
    permission_classes = (AllowAny,)
    renderer_classes = (BrowsableAPIRenderer, HALJSONRenderer, )


class PermissionViewSet(viewsets.ModelViewSet):
    model = Permission
    permission_classes = (AllowAny,)
    renderer_classes = (HALJSONRenderer,)

# WaterApp Models

class PWSSerializer(ModelSerializer):
    class Meta:
        model = PublicWaterSource

class PublicWaterSourceViewSet(viewsets.ModelViewSet):
    model = PublicWaterSource
    permission_classes = (AllowAny,)
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, )
    lookup_fields = ('id', 'pwsid', 'county')

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            val = self.kwargs.get(field)
            if val is not None:
                filter[field] = val

        return get_object_or_404(queryset, **filter)

    def list(self, request, *args, **kwargs):
        queryset = PublicWaterSource.objects.all()
        serializer = PWSSerializer(queryset, many=True)
        return Response(serializer.data)


class PublicWaterSourcesViewSet(viewsets.ModelViewSet):
    model = PublicWaterSource
    permission_classes = (AllowAny,)
    renderer_classes = (BrowsableAPIRenderer, HALJSONRenderer, )

    def by_county(self, request, *args, **kwargs):
        county = kwargs.get('county', '')
        pws_list = PublicWaterSource.objects.filter(county=county)
        return Response(pws_list)


class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        depth = 2

class ReportViewSet(viewsets.ModelViewSet):
    model = Report
    permission_classes = (AllowAny,)
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, PDFRenderer, )
    lookup_fields = ('id', 'pk')

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            val = self.kwargs.get(field)
            if val is not None:
                filter[field] = val

        return get_object_or_404(queryset, **filter)

    def list(self, request, *args, **kwargs):
        queryset = Report.objects.all()
        serializer = ReportSerializer(queryset, many=True)
        return Response(serializer.data)

    def by_source(self, request, *args, **kwargs):
        source = kwargs.get('source', '')
        report_list = PublicWaterSource.objects.filter(source=source)
        return Response(report__list)

