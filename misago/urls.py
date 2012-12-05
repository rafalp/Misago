from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from misago.admin import ADMIN_PATH, site

# Include frontend patterns
urlpatterns = patterns('',
    (r'^', include('misago.auth.urls')),
    (r'^users/', include('misago.profiles.urls')),
    (r'^usercp/', include('misago.usercp.urls')),
    (r'^register/', include('misago.register.urls')),
    (r'^activate/', include('misago.activation.urls')),
    (r'^reset-password/', include('misago.resetpswd.urls')),
    url(r'^$', 'misago.views.home', name="index"),
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