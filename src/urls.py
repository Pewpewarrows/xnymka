from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap
from django.views.generic.simple import direct_to_template

import nexus
from sitemaps import PagesSitemap

nexus.autodiscover()
admin.autodiscover()

sitemaps = {
    'pages': PagesSitemap,
    'flatpages': FlatPageSitemap,
}

urlpatterns = patterns('',
    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^nexus/', include(nexus.site.urls)),
    url(r'^sentry/', include('sentry.web.urls')),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {
        'sitemaps': sitemaps
    }),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {
        'sitemaps': sitemaps
    }),

    url(r'^$', direct_to_template, {'template': 'homepage.html'}, name='frontpage'),
    url(r'^demo/$', direct_to_template, {'template': 'demo.html'}, name='demo'),
)

if settings.MEDIA_DEV_MODE:
    #urlpatterns += patterns('django.views.static',
        #url(r'^%s(?P<path>.*)$' % settings.TAGGIT_AUTOCOMPLETE_MEDIA_URL[1:], 'serve', {
            #'document_root': settings.RAW_STATIC_ROOT + '/lib/taggit_autocomplete_modified/',
        #}),
    #)
    urlpatterns += patterns('django.views.static',
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )

