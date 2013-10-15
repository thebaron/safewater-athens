
from django.contrib.auth.models import User, Permission
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.permissions import AllowAny

from safewater.api.renderers import HALJSONRenderer, PDFRenderer
from safewater.constants import (
    SOURCE_CHOICES,
    REPORT_TYPE_CHOICES,
    REPORT_STATUS_CHOICES,
    SEVERITY_CHOICES,
    REPORT_VERIFICIATION_CHOICES
)
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
    source = serializers.ChoiceField(choices=SOURCE_CHOICES)

    pwsid = serializers.CharField(max_length=9)
    name = serializers.CharField(max_length=80)

    epa_region = serializers.CharField(max_length=2)
    geography_type = serializers.CharField(max_length=9)
    state = serializers.CharField(max_length=2)
    county = serializers.CharField(max_length=40)
    fips_county = serializers.CharField(max_length=5)
    regulating_agency_name = serializers.CharField(max_length=80)

    status = serializers.CharField(max_length=6)
    date_closed = serializers.DateField()
    pwstype = serializers.CharField(max_length=7)
    primary_source = serializers.CharField(max_length=3)
    primary_source_name = serializers.CharField(max_length=45)
    owner_type = serializers.CharField(max_length=14)

    contact_name = serializers.CharField(max_length=70)
    contact_org_name = serializers.CharField(max_length=80)
    contact_phone = serializers.CharField(max_length=15)
    contact_addr1 = serializers.CharField(max_length=50)
    contact_addr2 = serializers.CharField(max_length=50)
    contact_address = serializers.SerializerMethodField('get_combined_address')
    contact_city = serializers.CharField(max_length=40)
    contact_state = serializers.CharField(max_length=2)
    contact_zip = serializers.CharField(max_length=14)

    last_updated = serializers.DateTimeField()
    population_served = serializers.IntegerField(default=0)

    class Meta:
        model = PublicWaterSource



    def get_combined_address(self, obj):
        ret = obj.contact_addr1
        if obj.contact_addr2 is not None:
            ret = ret + '\n' + obj.contact_addr2

        return ret


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


    def retrieve(self, request, pk=None):
        queryset = PublicWaterSource.objects.get(pk=pk)
        serializer = PWSSerializer(queryset)
        return Response(serializer.data)

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

    source = serializers.ChoiceField(choices=SOURCE_CHOICES)
    source_uri = serializers.CharField(max_length=255)
    report_type = serializers.ChoiceField(choices=REPORT_TYPE_CHOICES)

    summary = serializers.CharField(max_length=255)
    date_reported = serializers.DateField()
    date_resolved = serializers.DateField()
    status = serializers.ChoiceField(choices=REPORT_STATUS_CHOICES)
    verification = serializers.ChoiceField(choices=REPORT_VERIFICIATION_CHOICES)
    severity = serializers.ChoiceField(choices=SEVERITY_CHOICES)
    description = serializers.CharField(max_length=1024)
    info_url1 = serializers.CharField(max_length=255)
    info_url2 = serializers.CharField(max_length=255)
    info_url3 = serializers.CharField(max_length=255)
    info_url4 = serializers.CharField(max_length=255)

    pws_affected = PWSSerializer()
    contaminant_name = serializers.CharField(max_length=255)
    contaminant_type = serializers.CharField(max_length=40)
    violation_type   = serializers.CharField(max_length=40)

    class Meta:
        model = Report
        depth = 2

        fields = ('id', 'source', 'source_uri', 'report_type',
            'pws_affected')


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

    def retrieve(self, request, pk=None):
        queryset = Report.objects.get(pk=pk)
        serializer = ReportSerializer(queryset)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = Report.objects.all()
        serializer = ReportSerializer(queryset, many=True)
        return Response(serializer.data)

    def by_source(self, request, *args, **kwargs):
        source = kwargs.get('source', '')
        report_list = PublicWaterSource.objects.filter(source=source)
        return Response(report__list)

