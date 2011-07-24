# Override any common settings, import the local private info not tracked in
# version control, and finally wrap-up the settings process.

from conf.common.settings import *

DEBUG = True
MEDIA_DEV_MODE = DEBUG
SSL_ENABLED = not DEBUG
CACHE_BACKEND = 'dummy:///'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# How much does this fuck up toolbar rendering? Might have to just hardcode
# where it needs to be in the middleware chain.
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar',)

# From: justcramer.com/2011/01/13/settings-in-django/
try:
    from local_settings import *
except ImportError:
    import sys, traceback
    sys.stderr.write("Warning: Can't find the file 'local_settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.stderr.write("\nFor debugging purposes, the exception was:\n\n")
    traceback.print_exc()

from conf.common.override import *
