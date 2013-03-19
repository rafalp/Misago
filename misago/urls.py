from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from misago.admin import ADMIN_PATH, site

# Include frontend patterns
urlpatterns = patterns('misago.apps',
    url(r'^$', 'index.index', name="index"),
    url(r'^read-all/$', 'readall.read_all', name="read_all"),
    url(r'^register/$', 'register.views.form', name="register"),
    url(r'^category/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', 'category.category', name="category"),
    url(r'^redirect/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', 'redirect.redirect', name="redirect"),
    url(r'^alerts/$', 'alerts.alerts', name="alerts"),
    url(r'^news/$', 'newsfeed.newsfeed', name="newsfeed"),
    url(r'^tos/$', 'tos.tos', name="tos"),
    url(r'^forum-map/$', 'forummap.forum_map', name="forum_map"),
    url(r'^popular/$', 'popularthreads.popular_threads', name="popular_threads"),
    url(r'^popular/(?P<page>[0-9]+)/$', 'popularthreads.popular_threads', name="popular_threads"),
    url(r'^new/$', 'newthreads.new_threads', name="new_threads"),
    url(r'^new/(?P<page>[0-9]+)/$', 'newthreads.new_threads', name="new_threads"),
)

urlpatterns += patterns('',
    (r'^', include('misago.apps.signin.urls')),
    (r'^users/', include('misago.apps.profiles.urls')),
    (r'^usercp/', include('misago.apps.usercp.urls')),
    (r'^activate/', include('misago.apps.activation.urls')),
    (r'^watched-threads/', include('misago.apps.watchedthreads.urls')),
    (r'^reset-password/', include('misago.apps.resetpswd.urls')),
    (r'^announcements/', include('misago.apps.announcements.urls')),
    #(r'^private-discussions/', include('misago.apps.privatethreads.urls')),
    #(r'^reports/', include('misago.apps.reports.urls')),
    (r'^', include('misago.apps.threads.urls')),
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
handler403 = 'misago.apps.errors.error403'
handler404 = 'misago.apps.errors.error404'
