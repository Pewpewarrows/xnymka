# Django settings for mymodernlife project.

# TODO: organize this file as such:
#   environment sys paths and media paths
#   authors, admins, managers, etc
#   debug vars
#   logging
#   cache
#   email
#   testing, coverage
#   database
#   sessions
#   middleware
#   templates
#   apps
#   third-party settings...

import sys
import os.path

PROJECT_ROOT = os.path.join(os.path.realpath(os.path.dirname(__file__)), '..', '..')

sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

DEFAULT_FROM_EMAIL = 'support@christina.com'

ADMINS = (
    ('Marco Chomut', 'marco.chomut+christina@gmail.com'),
)

MANAGERS = ADMINS

# Note that sensitive information, such as username/password/secretkey,
# are all stored in a separate settings file that is not tracked in git

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

INTERNAL_IPS = (
    '127.0.0.1',
)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, '..', 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/uploads/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'generated_static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

USE_ETAGS = False
PREPEND_WWW = False
DEBUG = False
MEDIA_DEV_MODE = DEBUG
TEMPLATE_DEBUG = True # Now that we have sentry, we always want that debug info

SESSION_COOKIE_HTTPONLY = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

if USE_I18N:
    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.i18n',)

# DO NOT modify the order of these, they have to wrap in a specific order
MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware', # Must be first
    'mediagenerator.middleware.MediaMiddleware',
    'dogslow.WatchdogMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'sentry.client.middleware.Sentry404CatchMiddleware',
    # 'django.middleware.transaction.TransactionMiddleware',    # Needed?
    'maintenancemode.middleware.MaintenanceModeMiddleware',
    'xframeoptions.middleware.Header',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

# Alternative:
"""
TEMPLATE_DIRS = ()
for root, dirs, files in os.walk(PROJECT_PATH):
    if 'templates' in dirs: TEMPLATE_DIRS += (os.path.join(root, 'templates'),)
"""

CACHE_MIDDLEWARE_SECONDS = 3600
CACHE_MIDDLEWARE_KEY_PREFIX = ''

INSTALLED_APPS = (
    # Included in Django
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    # 'django.contrib.databrowse', # read-only version of the admin
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.markup', # includes textile, markdown, ReST
    'django.contrib.messages',
    'django.contrib.redirects', # db-level redirects, as opposed to urlconfs
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    #'django.contrib.staticfiles',
    'django.contrib.syndication',
    'django.contrib.webdesign', # lorem ipsum generator

    # Third-Party
    'batch_select',
    'classytags',
    'django_extensions',
    # 'easy_thumbnails',
    'gargoyle',
    # 'indexer',
    # 'mailer',
    'mediagenerator',
    'nexus',
    # 'paging',
    'sentry',
    'sentry.client',
    'south',
    'test_utils',
    'typogrify',
    'xframeoptions',

    # Prometheus

    # Project-specific
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

# Custom Application Settings

LOGIN_REDIRECT_URL = '/'
# ACCOUNT_ACTIVATION_DAYS = 7

# AUTH_PROFILE_MODULE = 'profiles.UserProfile'

# COMMENTS_APP = 'my_comment_app'

TESTING = True

THUMBNAIL_SUBDIR = 'thumbs'

X_FRAME_OPTIONS = 'SAMEORIGIN'

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

MEDIA_BUNDLES = (
    ('main.css',
        #'css/lib/uni-form-generic.css',
        #'css/lib/uni-form.css',
        'css/reset.css',
        'css/scaffold.css',
        # 'css/base_theme.css',
        'css/christina.css',
        'lib/Aristo/jquery-ui-1.8.7.custom.css',
    ),
    ('main.js',
        'js/lib/json2.js',
        'js/lib/underscore.js',
        'js/lib/underscore.string.js',
        'js/lib/underscore.date.js',
        'js/lib/backbone.js',
        'js/utils.js',
        'js/christina.js',
    ),
    ('jquery.js',
        'js/lib/jquery-1.6.1.js',
    ),
    ('belatedpng.js',
        'js/lib/dd_belatedpng.js',
    ),
    ('modernizr.js',
        'js/lib/modernizr-2.0.4.js',
    ),
)

RAW_STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
GLOBAL_MEDIA_DIRS = (RAW_STATIC_ROOT,)

ROOT_MEDIA_FILTERS = {
    'css': 'mediagenerator.filters.yuicompressor.YUICompressor',
    'js': 'mediagenerator.filters.closure.Closure',
}

YUICOMPRESSOR_PATH = os.path.join(RAW_STATIC_ROOT, 'java/yuicompressor-2.4.2.jar')
CLOSURE_COMPILER_PATH = os.path.join(RAW_STATIC_ROOT, 'java/closure-compiler.jar')

DEV_MEDIA_URL = '/static/'
PRODUCTION_MEDIA_URL = '//static.christina.dotcloud.com/'

# Testing & Coverage

# Use nosetests instead of unittest
"""
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

COVERAGE_REPORT_HTML_OUTPUT_DIR = 'coverage'
COVERAGE_MODULE_EXCLUDES = ['tests$', 'settings$', 'urls$', 'vendor$',
        '__init__', 'migrations', 'templates', 'django', 'debug_toolbar',
        'core\.fixtures', 'users\.fixtures',]

try:
    import multiprocessing
    cpu_count = multiprocessing.cpu_count()
except ImportError:
    cpu_count = 1

NOSE_ARGS = ['--logging-clear-handlers', '--processes=%s' % cpu_count]

if is_solo():
    try:
        os.mkdir(COVERAGE_REPORT_HTML_OUTPUT_DIR)
    except OSError:
        pass
"""

# Message Broker (for Celery)
"""
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "boilerplate"
BROKER_PASSWORD = "boilerplate"
BROKER_VHOST = "boilerplate"
CELERY_RESULT_BACKEND = "amqp"

# Run tasks eagerly in development, so developers don't have to keep a celeryd
# processing running.
CELERY_ALWAYS_EAGER = is_solo()
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# South

# Speed up testing when you have lots of migrations.
SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True
"""

# Sessions

#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
