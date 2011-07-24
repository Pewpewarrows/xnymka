import os
import sys

WSGI_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(WSGI_ROOT, 'src'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'src.conf.prod.settings'

import django.core.handlers.wsgi
djangoapplication = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    if 'SCRIPT_NAME' in environ:
        del environ['SCRIPT_NAME']
    return djangoapplication(environ, start_response)
