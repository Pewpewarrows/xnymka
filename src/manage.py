#!/usr/bin/env python
from django.core.management import execute_manager

try:
    import conf.local.settings
except ImportError:
    import sys, traceback
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.stderr.write("\nFor debugging purposes, the exception was:\n\n")
    traceback.print_exc()
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(conf.local.settings)
