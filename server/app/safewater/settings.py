# Django settings for safewater project.

USE_X_FORWARDED_HOST = True

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Baron Chandler', 'baron@venturecranial.com'),
    ('Chris Sparnicht', 'chris@greenman.us')
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',

        'NAME': 'safewater',                      # Or path to database file if using sqlite3.
        'USER': 'safewater',                      # Not used with sqlite3.
        'PASSWORD': 'nocrypt0',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/opt/water/app/site/django-assets/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/django-assets/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'iBMqY,@CRE.s@8EcyaH[;1!x(YS]U8)<cT$e$!VD.Nj~IK0F+?D'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


if DEBUG:
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
        'chromelogger.DjangoMiddleware',
    )

ROOT_URLCONF = 'safewater.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'safewater.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/opt/water/app/safewater/templates',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)



INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'south',
    'gunicorn',
    'django_extensions',
    'rest_framework',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',

    'safewater',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',

    'djcelery',


    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        ],
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',
    'FILTER_BACKENDS': [
        'rest_framework.filters.DjangoFilterBackend',
        ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),

    'PAGINATE_BY': 10,
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = \
    { 'facebook':
        {
            'SCOPE': ['email', 'publish_stream'],
            'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
            'METHOD': 'oauth2',
            'LOCALE_FUNC': lambda request: 'en_US',
        },
    }

BROKER_URL = 'redis://'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_RESULT_BACKEND = 'redis://'

CELERY_ROUTES = {
                  "app.tasks.monitor_twitter": {"queue": "twitter"},
                  "app.tasks.import_violations":  {"queue" : "swdis"},
                  "app.tasks.import_pws" : {"queue":"swdis"}
                }


TWITTER_APP_KEY = 'ckZl3qrMckgFEHMrHHO1DQ'
TWITTER_APP_SECRET = 'rpEGs0mPGYnA79MdCTMmCr2dAS38SEMeCW2yM3o3E'


import djcelery
djcelery.setup_loader()


SWDIS_PWS_COUNTIES = ('OCONEE', 'CLARKE')
SWDIS_COUNTY_SERVED = 'http://iaspub.epa.gov/enviro/efservice/SDW_COUNTY_SERVED/STATE/GA/COUNTYSERVED/%s/JSON'
SWDIS_VIOLATIONS = 'http://iaspub.epa.gov/enviro/efservice/SDW_VIOL_ENFORCEMENT/COUNTYSERVED/%s/STATE/GA/COMPPERBEGINDATE/%%3E/31-DEC-2009/JSON'

try:
    from local_settings import *
except:
    pass


