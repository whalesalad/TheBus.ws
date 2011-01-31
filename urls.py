from django.conf.urls.defaults import *
from django.contrib import admin

from thebus.misc.feeds import UpdateFeed

feeds = {
    'updates': UpdateFeed,
}

admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^/?$', 'thebus.web.views.home', { 'template': 'home.html' }, name='home'),
    url(r'^q/$', 'thebus.web.views.search', { 'template': 'search_results.html' }),
    url(r'^location/(?P<latitude>\S*)/(?P<longitude>\S*)/$', 'thebus.web.views.search_by_location', { 'template': 'location_results.html' }),
    
    url(r'^s:(?P<stop_id>\d+)/$', 'thebus.web.views.stop_detail', { 'template': 'stop_detail.html' }),
    url(r'^r:(?P<route_short_name>(\D*\d*))/$', 'thebus.web.views.route_detail', { 'template': 'route_detail.html' }),
    url(r'^b:(?P<bus_number>(\d*))/$', 'thebus.web.views.bus_detail', { 'template': 'bus_detail.html' }),
    
    url(r'^about/$', 'thebus.web.views.home', { 'template': 'about.html' }, name='about'),
    
    url(r'^updates/$', 'thebus.web.views.updates', { 'template': 'updates.html' }, name='updates'),
    url(r'^updates/(?P<update_slug>(\D*\d*))/$', 'thebus.web.views.update_detail', { 'template': 'update_detail.html' }, name='update-detail'),
    
    url(r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', { 'feed_dict': feeds }, name='feeds'),
    
    url(r'^feedback/$', 'thebus.web.views.feedback', { 'template': 'feedback.html' }, name='feedback'),

    # Django admin shiz
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
