# Override any common settings, import the local private info not tracked in
# version control, and finally wrap-up the settings process.

from conf.common.settings import *

DEBUG = True
MEDIA_DEV_MODE = False
SSL_ENABLED = not DEBUG
CACHE_BACKEND = 'dummy:///'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, '..', '..', 'uploads')

STATIC_URL = '//static.christina.dotcloud.com/'

#TAGGIT_AUTOCOMPLETE_MEDIA_URL = PRODUCTION_MEDIA_URL + 'taggit_autocomplete_modified/'

# From: justcramer.com/2011/01/13/settings-in-django/
try:
    from local_settings import *
except ImportError:
    import sys, traceback
    sys.stderr.write("Warning: Can't find the file 'local_settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.stderr.write("\nFor debugging purposes, the exception was:\n\n")
    traceback.print_exc()

from conf.common.override import *
