# We're providing two places for site administrators to override settings
# if they need to, which will allow them to change things without having to
# redeploy the entire site. The first is from environment variables, the second
# from a yaml config file outside of the project root.

import os

# From: justcramer.com/2011/01/13/settings-in-django/
DJANGO_CONF = os.environ.get('DJANGO_CONF', 'default')
if DJANGO_CONF != 'default':
    module = __import__(DJANGO_CONF, globals(), locals(), ['*'])
    for k in dir(module):
        locals()[k] = getattr(module, k)

# From: github.com/garethr/django-project-templates
settings_override = "/etc/nrshirts.yml"
try:
    file = open(settings_override)
    for key, value in yaml.load(file).items():
        globals()[key]=value
except:
    # we don't always have the file around or need the setting
    # defined so best to be quite if things go wrong
    pass

# From: justcramer.com/2011/01/13/settings-in-django/
# Finally, if we want anyting explicitly disabled, this allows for it
if 'DISABLED_APPS' in locals():
    INSTALLED_APPS = [k for k in INSTALLED_APPS if k not in DISABLED_APPS]

    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
    DATABASE_ROUTERS = list(DATABASE_ROUTERS)
    TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS)

    for a in DISABLED_APPS:
        for x, m in enumerate(MIDDLEWARE_CLASSES):
            if m.startswith(a):
                MIDDLEWARE_CLASSES.pop(x)

        for x, m in enumerate(TEMPLATE_CONTEXT_PROCESSORS):
            if m.startswith(a):
                TEMPLATE_CONTEXT_PROCESSORS.pop(x)

        for x, m in enumerate(DATABASE_ROUTERS):
            if m.startswith(a):
                DATABASE_ROUTERS.pop(x)
