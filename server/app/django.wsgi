import os
import sys
path = '/opt/water/app'
if path not in sys.path:
    sys.path.append(path)

path = '/opt/water/var/lib/python2.7/site-packages/'

import site
site.addsitedir(path)



os.environ['DJANGO_SETTINGS_MODULE'] = 'safewater.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

