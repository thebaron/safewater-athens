import time
import os
import simplejson as json
import requests

from datetime import datetime

from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings

from safewater.models import PublicWaterSource, Report, Action
from safewater.constants import (
    SOURCE_EPA,

    REPORT_TYPE_VIOLATION,
    REPORT_STATUS_OPEN,
    REPORT_STATUS_RESOLVED,
    REPORT_VERIFICATION_VERIFIED,

    SEVERITY_UNSPECIFIED,

    ACTION_ENTITY_EPA,
    ACTION_TYPE_ENFORCEMENT,
    ACTION_STATUS_COMPLETE,
)


class Swdis:

    """
        Class to handle Safe Water EPA APIs
    """

    _log = '\n'
    stdout_log = False

    def log(self, msg):
        self._log = self._log + msg + '\n'
        if self.stdout_log:
            print msg

    def get_log(self):
        return self._log

    def convert_date(self, datein):
        if datein is None:
            return ''
        return datetime.strptime(datein, '%d-%b-%y').strftime('%Y-%m-%d')

    #pwsid is not used right now
    def import_pws(self, pwsid=None):

        """
            Suck in the list of public water sources for each county.
        """

        for county in settings.SWDIS_PWS_COUNTIES:

            self.log('Fetching sources in %s county...' % (county))

            url = settings.SWDIS_COUNTY_SERVED % (county)
            # url = 'http://iaspub.epa.gov/enviro/efservice/SDW_COUNTY_SERVED/STATE/GA/COUNTYSERVED/%s/JSON' % (county)

            req = requests.get(url)
            if (req.status_code == 200):

                self.log(' OK!')

                newSources = 0

                for row in req.json():

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
                    if created:
                        newSources = newSources + 1
                    m.save()

                if newSources > 0:
                    self.log('%d new sources were added.' % (newSources))

            else:
                self.log(' FAIL (status %d)' % (req.status_code))


        self.log('Updating %d public water sources...' % (PublicWaterSource.objects.count()))

        for pws in PublicWaterSource.objects.all():
            self.log('Fetching PWSID %s... ' % (pws.pwsid))
            url = 'http://iaspub.epa.gov/enviro/efservice/PWS/PWSID/%s/JSON' %(pws.pwsid)

            req = requests.get(url)
            if req.status_code == 200:
                json = req.json()
                if len(json) != 1:
                    self.log(' OK, but invalid JSON returned')
                else:
                    self.log(' OK!')

                row = json[0]
                pws.epa_region = row.get('EPA_REGION', '')
                pws.geography_type = row.get('GEOGRAPHY_TYPE', '')
                pws.status = row.get('STATUS', '')
                dd = self.convert_date(row.get('PWSDEACTIVATIONDATE', ''))
                if dd != '':
                    pws.date_closed = dd
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
            else:
                self.log(' FAIL (status %d)' % (req.status_code))
            pws.save()

        self.log('Task complete.')
        return self.get_log()

    def import_violations(self):
        """
            Suck in the violations from the EPA
        """

        newViolations = 0
        newActions = 0

        for county in { item['county'] for item in PublicWaterSource.objects.values('county') }:

            self.log('Fetching violations for %s county...' % (county))

            # FIXME: date needs work
            url = settings.SWDIS_VIOLATIONS % (county)

            # 'http://iaspub.epa.gov/enviro/efservice/SDW_VIOL_ENFORCEMENT/COUNTYSERVED/%s/STATE/GA/COMPPERBEGINDATE/%%3E/31-DEC-2009/JSON' % (county)

            req = requests.get(url)

            if (req.status_code == 200):

                response_json = req.json()

                self.log(' OK!%d violations found.' % len(response_json))
                newViolations = 0

                for row in response_json:

                    self.log('    > %s-%s' % (row.get('VNAME', 'Unknown )violation'), row.get('COMPPERBEGINDATE', '')))

                    pws = PublicWaterSource.objects.get(pwsid=row.get('PWSID'))

                    report, created = Report.objects.get_or_create(
                        source = SOURCE_EPA,
                        source_uri = url,
                        report_type = REPORT_TYPE_VIOLATION,
                        summary = row.get('VNAME', 'Unknown violation'),
                        date_reported = self.convert_date(row.get('COMPPERBEGINDATE', '')),
                        date_resolved = self.convert_date(row.get('COMPPERENDDATE', '')),
                        status = REPORT_STATUS_OPEN,
                        verification = REPORT_VERIFICATION_VERIFIED,
                        severity = SEVERITY_UNSPECIFIED,
                        description = 'Sources: %s\n\nDefinition: %s\n\nHealth Effects: %s' % (row.get('SOURCES', 'Unspecified'), row.get('DEFINITION', 'Unspecified'), row.get('HEALTH_EFFECTS', 'Unspecified')),
                        pws_affected = pws,
                        contaminant_name = row.get('CNAME', '').strip(),
                        contaminant_type = row.get('CTYPE', '').strip(),
                        violation_type = row.get('VTYPE', '').strip(),
                    )
                    if created:
                        newViolations = newViolations + 1

                    action, created = Action.objects.get_or_create(
                        source = SOURCE_EPA,
                        source_uri = url,

                        summary = row.get('ENFACTIONNAME', '').strip(),
                        status = ACTION_STATUS_COMPLETE,
                        date_taken = self.convert_date(row.get('ENFDATE', '')),

                        entity = ACTION_ENTITY_EPA,
                        action_type = ACTION_TYPE_ENFORCEMENT,
                        action_subtype = row.get('ENFACTIONTYPE', '').strip(),

                        report = report
                        )

                    if created:
                        newActions = newActions + 1

                    # per the quick start doc, enf action types of
                    # FOX, EOX, and SOX indicate the compliance was
                    # achieved.
                    #
                    # We can then say the report was "resolved."
                    #
                    if (action.action_subtype == 'EOX' or
                        action.action_subtype == 'FOX' or
                        action.action_subtype == 'SOX'):
                        report.status = REPORT_STATUS_RESOLVED
                        report.save()


                if (newViolations > 0):
                    self.log('%d new violations recorded.' % (newViolations))
                if (newActions > 0):
                    self.log('%d new actions recorded.' % (newActions))

            else:
                self.log(' FAIL (status %d)' % (req.status_code))

        return self.get_log()

