# Django settings for temp project.

# set up a shortcut for the base location of the project
import os
import os.path
import sys

PROJECT_PATH = os.path.abspath(os.path.split(os.path.split(__file__)[0])[0])

# add the lib directory to the path
sys.path.insert(0, os.path.join(PROJECT_PATH, 'lib'))

# DMIGRATIONS_DIR = os.path.join(PROJECT_PATH, 'migrations')

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
INTERNAL_IPS = ('127.0.0.1', )
IGNORABLE_404_STARTS = ('/favicon.ico', )

ADMINS = (
    ('Dana Spiegel', 'dana@nycwireless.net'),
)

MANAGERS = (
    ('Dana Spiegel', 'dana@nycwireless.net'),
)

DATABASE_ENGINE = 'mysql'
DATABASE_OPTIONS = {
    'init_command': 'SET storage_engine=INNODB',
    'use_unicode': True,
    'charset': 'utf8', 
}


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    # 'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django_announcements.context_processors.site_wide_announcements',
    'breakout.context_processors.sidebar',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'middleware.wsgi_exceptions.WsgiLogErrors',
    'middleware.debug.DebugFooter',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    # 'django.contrib.csrf.middleware.CsrfMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'middleware.google_analytics.GoogleAnalyticsMiddleware',
    'django_pagination.middleware.PaginationMiddleware',
    'breakout.middleware.BreakoutMiddleware',
    'middleware.iphone.iPhoneMiddleware',
)

AUTHENTICATION_BACKENDS = (
    # 'account.authentication_backends.TwitterBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# include all templates that are in the applications on the project path
TEMPLATE_DIRS = ()
for root, dirs, files in os.walk(PROJECT_PATH):
    if 'templates' in dirs: TEMPLATE_DIRS = TEMPLATE_DIRS + (os.path.join(root, 'templates'),)

SITE_ID = 1
ROOT_URLCONF = 'urls'

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin/media/'

# set the session cookie age programmatically
# (seconds/minute) * (minutes/hour) * (hours/day) * (days/year)
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365

DEFAULT_FROM_EMAIL = 'no-reply@breakoutfestival.org'
SERVER_EMAIL = 'server@breakoutfestival.org'

AUTH_PROFILE_MODULE = 'account.UserProfile'
LOGIN_REDIRECT_URL = '/'

CONSUMER_KEY = 'i7jNBFeCfpLgLgxuxCuA'
CONSUMER_SECRET = 'TzYNIUtvemCkKWUjwlB8S4GAsabqcWQvQiIneYX6gw'

ANALYTICS_ID = 'UA-5053085-4'
ANALYTICS_IGNORE_ADMIN = True

ACCOUNT_ACTIVATION_DAYS = 14

FILE_UPLOAD_PERMISSIONS = 0644

# Django-tagging-ng settings
FORCE_LOWERCASE_TAGS = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'django_announcements',
    'django_robots',
    'django_extensions',
    'django_chronograph',
    'django_pagination',
    'django_mailer',
    'tinymce',
    'contact_form',
    # 'registration',
    # 'south',
    'twitter_app',
    'account',
    'breakout',
    'lifestream',
    'tagging',
)
