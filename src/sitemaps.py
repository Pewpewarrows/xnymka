import datetime

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

# http://somedot.com/development/2008/03/django-sitemap/
#
# Allows you to generate sitemap.xml info for pages that aren't in an app,
# but aren't just flatpages.
class PagesSitemap(Sitemap):
    pages = {
        """
        'name': {
            'priority': 1,
            'url_name': 'reverse_name',
            'modified': '',
            'changefreq': 'never',
            'args': {},
        },
        """
        
        'Home': {
            'priority': 1.0,
            'url_name': 'frontpage',
            'changefreq': 'never',
        },
        'Demo': {
            'priority': 0.9,
            'url_name': 'demo',
            'changefreq': 'never',
        },
    }
    
    def items(self):
        return self.pages.keys()
        
    def location(self, obj):
        page = self.pages[obj]
        return page.get('uri') or reverse(page['url_name'], **page.get('args', {}))
        
    def lastmod(self, obj):
        return datetime.datetime.now() # until I think of something better
        
    def priority(self, obj):
        page = self.pages[obj]
        return page.get('priority', 0.5)
        
    def changefreq(self, obj):
        page = self.pages[obj]
        return page.get('changefreq', 'never')
