import time
import os
import simplejson as json
import requests

from datetime import datetime

from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings

from safewater.models import PublicWaterSource, Report
from safewater.constants import (
    SOURCE_EPA,
    REPORT_TYPE_VIOLATION,
    REPORT_STATUS_RESOLVED,
    REPORT_VERIFICATION_VERIFIED,
    SEVERITY_UNSPECIFIED
)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--import-pws',
            action="store_true", dest="import_pws", default=False,
            help="Import EPA PWS data"
        ),
        make_option(
            '--import-violations',
            action="store_true", dest="import_violations", default=False,
            help="Import EPA Violation and Enforcement data"
        ),
    )

    def handle(self, *test_labels, **options):

        if options['import_pws']:
            self.import_pws(options.get('pws_id'))
            return

        if options['import_violations']:
            self.import_violations(options.get('pws_id'))
            return

    def convert_date(self, datein):
        return datetime.strptime(datein, '%d-%b-%y').strftime('%Y-%m-%d')

    def import_pws(self, pwsid): #pwsid is not ised right now

        for county in ('OCONEE', 'CLARKE'):

            print 'Fetching %s county...' % (county)

            url = 'http://iaspub.epa.gov/enviro/efservice/SDW_COUNTY_SERVED/STATE/GA/COUNTYSERVED/%s/JSON' % (county)

            req = requests.get(url)
            assert req.status_code == 200, 'status code not OK'

            for row in req.json():

                # import pdb; pdb.set_trace()

                m, created = PublicWaterSource.objects.get_or_create(
                    source = SOURCE_EPA,
                    pwsid = row.get('PWSID'))

                m.name = row.get('PWSNAME', '')
                m.state = row.get('STATE', '')
                m.county = county # row.get('COUNTYSERVED', '')
                m.regulating_agency_name = row.get('REGULATINGAGENCYNAME', '')

                m.contact_name = row.get('CONTACT', '')
                m.contact_phone = row.get('CONTACTPHONE', '')
                m.population_served = row.get('POPULATIONSERVED', 0)
		m.save()


        for pws in PublicWaterSource.objects.all():
            print 'Fetching PWSID %s...' % (pws.pwsid)
            url = 'http://iaspub.epa.gov/enviro/efservice/PWS/PWSID/%s/JSON' %(pws.pwsid)
            req = requests.get(url)
            if req.status_code == 200:
                json = req.json()
                assert len(json) == 1

                row = json[0]
                pws.epa_region = row.get('EPA_REGION', '')
                pws.geography_type = row.get('GEOGRAPHY_TYPE', '')
                pws.status = row.get('STATUS', '')
                pws.date_closed = self.convert_date(row.get('PWSDEACTIVATIONDATE', '')),
                pws.pwstype = row.get('PWSTYPE', '')
                pws.primary_source = row.get('PSOURCE', '')
                pws.primary_source_name = row.get('PSOURCE_LONGNAME', '')
                pws.owner_type = row.get('OWNER', '')

                pws.contact_org_name = row.get('CONTACTORGNAME', '')
                pws.contact_addr1 = row.get('CONTACTADDRESS1', '')
                pws.contact_addr2 = row.get('CONTACTADDRESS2', '')
                pws.contact_city = row.get('CONTACTCITY', '')
                pws.contact_state = row.get('CONTACTSTATE', '')
                pws.contact_zip = row.get('CONTACTZIP', '')

                pws.save()

    def import_violations(self, id):
        """
            Suck in the violations from the EPA
        """
        for county in {item['county'] for item in PublicWaterSource.objects.values('county')}:

            print 'Fetching violations for %s county...' % (county)

            # FIXME: date needs work
            url = 'http://iaspub.epa.gov/enviro/efservice/SDW_VIOL_ENFORCEMENT/COUNTYSERVED/%s/STATE/GA/COMPPERBEGINDATE/%%3E/31-DEC-2009/JSON' % (county)

            req = requests.get(url)
            assert req.status_code == 200, 'status code not OK for url: %s' % (url)

            for row in req.json():

                print 'Processing violation %s-%s' % (row.get('VNAME', 'Unknown violation'), row.get('COMPPERBEGINDATE', ''))
                pws = PublicWaterSource.objects.get(pwsid=row.get('PWSID'))

                report, created = Report.objects.get_or_create(
                    source = SOURCE_EPA,
                    source_uri = url,
                    report_type = REPORT_TYPE_VIOLATION,
                    summary = row.get('VNAME', 'Unknown violation'),
                    date_reported = self.convert_date(row.get('COMPPERBEGINDATE', '')),
                    date_resolved = self.convert_date(row.get('COMPPERENDDATE', '')),
                    status = REPORT_STATUS_RESOLVED,
                    verification = REPORT_VERIFICATION_VERIFIED,
                    severity = SEVERITY_UNSPECIFIED,
                    description = 'Sources: %s\n\nDefinition: %s\n\nHealth Effects: %s' % (row.get('SOURCES', 'Unspecified'), row.get('DEFINITION', 'Unspecified'), row.get('HEALTH_EFFECTS', 'Unspecified')),
                    pws_affected = pws,
                    contaminant_name = row.get('CNAME', ''),
                    contaminant_type = row.get('CTYPE', ''),
                    violation_type = row.get('VTYPE', ''),
                 )


