
from django.db import models

from safewater.constants import (
    SOURCE_CHOICES,
    REPORT_TYPE_CHOICES,
    REPORT_STATUS_CHOICES,
    SEVERITY_CHOICES,
    REPORT_VERIFICIATION_CHOICES,
    ACTION_ENTITY_CHOICES,
    ACTION_TYPE_CHOICES,
    ACTION_STATUS_CHOICES,
)


class PublicWaterSource(models.Model):
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES)

    pwsid = models.CharField(max_length=9, unique=True)
    name = models.CharField(max_length=80, null=True)

    epa_region = models.CharField(max_length=2, null=True)
    geography_type = models.CharField(max_length=9, null=True)
    state = models.CharField(max_length=2, null=True)
    county = models.CharField(max_length=40, null=True)
    fips_county = models.CharField(max_length=5, null=True)
    regulating_agency_name = models.CharField(max_length=80, null=True)

    status = models.CharField(max_length=6, null=True)
    date_closed = models.DateField(null=True)
    pwstype = models.CharField(max_length=7, null=True)
    primary_source = models.CharField(max_length=3, null=True)
    primary_source_name = models.CharField(max_length=45, null=True)
    owner_type = models.CharField(max_length=14, null=True)

    contact_name = models.CharField(max_length=70, null=True)
    contact_org_name = models.CharField(max_length=80, null=True)
    contact_phone = models.CharField(max_length=15, null=True)
    contact_addr1 = models.CharField(max_length=50, null=True)
    contact_addr2 = models.CharField(max_length=50, null=True)
    contact_city = models.CharField(max_length=40, null=True)
    contact_state = models.CharField(max_length=2, null=True)
    contact_zip = models.CharField(max_length=14, null=True)

    population_served = models.IntegerField(null=True, default=0)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '(%s) %s' % (
            self.pwsid,
            self.name
        )

class Report(models.Model):
    """
    Models a report about a given public water system.
    """

    source = models.CharField(max_length=16, null=True, choices=SOURCE_CHOICES)
    source_uri = models.CharField(max_length=255)
    report_type = models.CharField(max_length=16, null=True, choices=REPORT_TYPE_CHOICES)
    summary = models.CharField(max_length=255, null=True)
    date_reported = models.DateField(null=True)
    date_resolved = models.DateField(null=True)
    status = models.CharField(max_length=16, choices=REPORT_STATUS_CHOICES)
    verification = models.CharField(max_length=16, choices=REPORT_VERIFICIATION_CHOICES)
    severity = models.CharField(max_length=16, null=True, choices=SEVERITY_CHOICES)
    description = models.CharField(max_length=1024, null=True)
    info_url1 = models.CharField(max_length=255, null=True)
    info_url2 = models.CharField(max_length=255, null=True)
    info_url3 = models.CharField(max_length=255, null=True)
    info_url4 = models.CharField(max_length=255, null=True)

    pws_affected = models.ForeignKey('PublicWaterSource')
    contaminant_name = models.CharField(max_length=255, null=True)
    contaminant_type = models.CharField(max_length=40, null=True)
    violation_type   = models.CharField(max_length=40, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s REPORT - %s\n    affects PWSID %s' % (
            self.source,
            self.summary,
            self.pws_affected.pwsid
        )

class Action(models.Model):
    """
    Models a set of actions taken as a result of a report.
    """

    class Meta:
        # -- put this back later
	# unique_together = (("entity", "action_type", "action_subtype", "report"),)

    source = models.CharField(max_length=16, null=True, choices=SOURCE_CHOICES)
    source_uri = models.CharField(max_length=255)

    summary = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=16, choices=ACTION_STATUS_CHOICES)
    date_taken = models.DateField(null=True)
    log = models.CharField(max_length=1024, blank=True, null=True)

    entity = models.CharField(max_length=32, null=True, choices=ACTION_ENTITY_CHOICES)
    action_type = models.CharField(max_length=16, null=True, choices=ACTION_TYPE_CHOICES)
    action_subtype = models.CharField(max_length=32, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    report = models.ForeignKey('Report')

    def __unicode__(self):
        return '%s ACTION - %s\n    against report (%d) %s' % (
            self.source,
            self.summary,
            self.report.id,
            self.report.summary
        )
