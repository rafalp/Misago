from django.conf import settings
from django.conf.urls import include, patterns, url
from django.utils.importlib import import_module

urlpatterns = patterns('misago.usercp.views',
    url(r'^credentials/$', 'credentials', name="usercp_credentials"),
    url(r'^username/$', 'username', name="usercp_username"),
    url(r'^signature/$', 'signature', name="usercp_signature"),
    url(r'^ignored/$', 'ignored', name="usercp_ignored"),
)

for extension in settings.USERCP_EXTENSIONS:
    urlpatterns += patterns('',
        (r'^', include(extension + '.urls')),
    )