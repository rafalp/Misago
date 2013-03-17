from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from misago.admin import ADMIN_PATH, site

# Include frontend patterns
urlpatterns = patterns('misago.apps.front',
    url(r'^$', 'index.index', name="index"),
    url(r'^read-all/$', 'readall.read_all', name="read_all"),
)

# Include shared Sign-In action
urlpatterns += patterns('',
    (r'^', include('misago.apps.signin.urls')),
    # Remove after ACP was refactored
    url(r'^users/(?P<username>\w+)-(?P<user>\d+)/$', 'misago.apps.admin.adminindex.todo', name="user"),    
)

"""
(r'^users/', include('misago.profiles.urls')),
(r'^usercp/', include('misago.usercp.urls')),
(r'^register/', include('misago.register.urls')),
(r'^activate/', include('misago.activation.urls')),
(r'^reset-password/', include('misago.resetpswd.urls')),
(r'^', include('misago.threads.urls')),
(r'^', include('misago.watcher.urls')),
url(r'^category/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', 'misago.views.category', name="category"),
url(r'^redirect/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', 'misago.views.redirection', name="redirect"),
url(r'^alerts/$', 'misago.alerts.views.show_alerts', name="alerts"),
url(r'^news/$', 'misago.newsfeed.views.newsfeed', name="newsfeed"),
url(r'^tos/$', 'misago.tos.views.forum_tos', name="tos"),
url(r'^forum-map/$', 'misago.views.forum_map', name="forum_map"),
url(r'^popular/$', 'misago.views.popular_threads', name="popular_threads"),
url(r'^popular/(?P<page>[0-9]+)/$', 'misago.views.popular_threads', name="popular_threads"),
url(r'^new/$', 'misago.views.new_threads', name="new_threads"),
url(r'^new/(?P<page>[0-9]+)/$', 'misago.views.new_threads', name="new_threads"),
"""

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
handler403 = 'misago.apps.views.error403'
handler404 = 'misago.apps.views.error404'
