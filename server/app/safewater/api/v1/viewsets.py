
from django.contrib.auth.models import User, Permission
from django.core.exceptions import MultipleObjectsReturned
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
    REPORT_VERIFICIATION_CHOICES,
    ACTION_TYPE_CHOICES,
    ACTION_STATUS_CHOICES,
)
from safewater.models import PublicWaterSource, Report, Action


# Django Models

class UserViewSet(viewsets.ModelViewSet):
    model = User
    permission_classes = (AllowAny,)
    renderer_classes = (BrowsableAPIRenderer, HALJSONRenderer, )


class PermissionViewSet(viewsets.ModelViewSet):
    model = Permission
    permission_classes = (AllowAny,)
    renderer_classes = (HALJSONRenderer,)


# Serializers


class ActionSerializer(ModelSerializer):

    _link = serializers.HyperlinkedRelatedField(read_only=True,
        view_name='action-detail', source='*')

    source = serializers.ChoiceField(choices=SOURCE_CHOICES)
    source_uri = serializers.CharField(max_length=255)

    summary = serializers.CharField(max_length=255)
    status = serializers.ChoiceField(choices=ACTION_STATUS_CHOICES)
    date_taken = serializers.DateField()
    log = serializers.CharField(max_length=1024)

    action_type = serializers.ChoiceField(choices=ACTION_TYPE_CHOICES)
    action_subtype = serializers.CharField()

    date_created = serializers.DateField()
    last_updated = serializers.DateField()

    report_uri = serializers.HyperlinkedRelatedField(read_only=True,
        view_name='report-detail', source='report')

    class Meta:
        model = Report
        depth = 1

        fields = ('_link', 'id', 'source', 'source_uri',
            'summary', 'status', 'date_taken', 'log',
            'action_type', 'action_subtype',
            'date_created', 'last_updated', 'report_uri')


class ReportSerializer(ModelSerializer):

    _link = serializers.HyperlinkedRelatedField(read_only=True,
        view_name='report-detail', source='*')

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

    pws_uri = serializers.HyperlinkedRelatedField(read_only=True,
        view_name='pws-detail', source='pws_affected')
    contaminant_name = serializers.CharField(max_length=255)
    contaminant_type = serializers.CharField(max_length=40)
    violation_type   = serializers.CharField(max_length=40)

    date_created = serializers.DateTimeField()
    last_updated = serializers.DateTimeField()

    class Meta:
        model = Report
        depth = 1

        fields = ('_link', 'id', 'source', 'source_uri', 'report_type',
            'pws_uri', 'summary', 'date_reported', 'date_resolved',
            'status', 'verification', 'severity', 'description',
            'info_url1', 'info_url2', 'info_url3', 'info_url4',
            'contaminant_name', 'contaminant_type', 'violation_type',
            'date_created', 'last_updated')


class PWSSerializer(ModelSerializer):

    _link = serializers.HyperlinkedRelatedField(read_only=True,
        view_name='pws-detail', source='*')

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
    date_created = serializers.DateTimeField()
    population_served = serializers.IntegerField(default=0)

    class Meta:
        model = PublicWaterSource
        fields = ('_link', 'id', 'source', 'pwsid', 'name', 'epa_region',
        'geography_type', 'state', 'county', 'fips_county',
        'regulating_agency_name', 'status', 'date_closed',
        'pwstype', 'primary_source', 'primary_source_name',
        'owner_type', 'contact_name', 'contact_org_name',
        'contact_phone', 'contact_address', 'contact_addr1',
        'contact_addr2', 'contact_city', 'contact_state', 'contact_zip',
        'population_served',
        'last_updated', 'date_created')

    def get_combined_address(self, obj):
        """Take the two-line address and make one crlf blob string."""
        alist = [addr or "" for addr in [obj.contact_addr1, obj.contact_addr2]]
        ret = '\n'.join(alist)
        return ret.strip()


###
### VIEW SETS
###

class PublicWaterSourceViewSet(viewsets.ModelViewSet):
    model = PublicWaterSource
    serializer_class = PWSSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,
        HALJSONRenderer, PDFRenderer)
    lookup_fields = ('pk', 'pwsid',)
    filter_fields = ('county', 'state', 'status', 'source',
            'epa_region', )

    def get_queryset(self):
        filter = {}
        for field in self.lookup_fields:
            val = self.kwargs.get(field)
            if val is not None:
                filter[field] = val
        return PublicWaterSource.objects.filter(**filter)

    def retrieve(self, request, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        if (queryset.count() != 1):
            return Response(status=404)
        serializer = PWSSerializer(queryset.get(), context={'request' : request})
        serializer.fields['reports'] = ReportSerializer(many=True,
        read_only=True, source='report_set')

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = PWSSerializer(queryset, many=True, context={'request' : request})
        serializer.fields['reports'] = serializers.HyperlinkedRelatedField(many=True, view_name='report-detail', source='report_set')
        return Response(serializer.data)


class ReportViewSet(viewsets.ModelViewSet):
    model = Report
    permission_classes = (AllowAny,)
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, PDFRenderer, )
    lookup_fields = ('id', 'pk')
    filter_fields = ('source', 'pws_affected__id',
        'pws_affected__pwsid', 'violation_type',
        'contaminant_type',)

    def get_queryset(self):
        filter = {}
        for field in self.lookup_fields:
            val = self.kwargs.get(field)
            if val is not None:
                filter[field] = val
        return Report.objects.filter(**filter)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        if (queryset.count() != 1):
            return Response(status=404)

        serializer = ReportSerializer(queryset.get(), context={'request' : request})
        serializer.fields['actions'] = ActionSerializer(many=True, read_only=True, source='action_set')
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = ReportSerializer(queryset, many=True, context={'request' : request})
        serializer.fields['actions'] = serializers.HyperlinkedRelatedField(many=True, source='action_set', view_name='action-detail')
        return Response(serializer.data)


class ActionViewSet(viewsets.ModelViewSet):
    model = Action
    permission_classes = (AllowAny,)
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, PDFRenderer, )
    lookup_fields = ('id', 'pk')
    filter_fields = ('source', 'report__pws_affected__id',
        'report__pws_affected__pwsid', 'action_type',
        'status', 'action_subtype')

    def get_queryset(self):
        filter = {}
        for field in self.lookup_fields:
            val = self.kwargs.get(field)
            if val is not None:
                filter[field] = val
        return Action.objects.filter(**filter)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        if (queryset.count() != 1):
            return Response(status=404)

        serializer = ActionSerializer(queryset.get(), context={'request' : request})
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = ActionSerializer(queryset, many=True, context={'request' : request})
        return Response(serializer.data)

