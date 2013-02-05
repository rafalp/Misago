from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from misago.admin import ADMIN_PATH, site

# Include frontend patterns
urlpatterns = patterns('',
    (r'^', include('misago.authn.urls')),
    (r'^users/', include('misago.profiles.urls')),
    (r'^usercp/', include('misago.usercp.urls')),
    (r'^register/', include('misago.register.urls')),
    (r'^activate/', include('misago.activation.urls')),
    (r'^reset-password/', include('misago.resetpswd.urls')),
    (r'^', include('misago.threads.urls')),
    url(r'^category/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', 'misago.views.category', name="category"),
    url(r'^redirect/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', 'misago.views.redirection', name="redirect"),
    url(r'^$', 'misago.views.home', name="index"),
    url(r'^alerts/$', 'misago.alerts.views.show_alerts', name="alerts"),
    url(r'^news/$', 'misago.newsfeed.views.newsfeed', name="newsfeed"),
    url(r'^tos/$', 'misago.tos.views.forum_tos', name="tos"),
    url(r'^read/$', 'misago.views.read_all', name="read_all"),
    url(r'^forum-map/$', 'misago.views.forum_map', name="forum_map"),
)

# Include admin patterns
if ADMIN_PATH:
    urlpatterns += patterns('',
        url(r'^' + ADMIN_PATH, include(site.discover())),
    )

# Include static and media patterns in DEBUG
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )

# Set error handlers
handler403 = 'misago.views.error403'
handler404 = 'misago.views.error404'
