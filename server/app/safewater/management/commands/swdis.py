import time
import os
import simplejson as json
import requests

from datetime import datetime

from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings

from safewater.constants import (
    SOURCE_EPA,
    REPORT_TYPE_VIOLATION,
    REPORT_STATUS_RESOLVED,
    REPORT_VERIFICATION_VERIFIED,
    SEVERITY_UNSPECIFIED
)
from safewater.models import PublicWaterSource, Report
from safewater.tasks import Swdis

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
            swdis = Swdis()
            swdis.stdout_log = True
            swdis.import_pws()
            return

        if options['import_violations']:
            swdis = Swdis()
            swdis.stdout_log = True
            swdis.import_violations()
            return

    def convert_date(self, datein):
        return datetime.strptime(datein, '%d-%b-%y').strftime('%Y-%m-%d')



