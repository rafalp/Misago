from django.conf.urls import patterns, url, include
from misago.admin import ADMIN_PATH

urlpatterns = patterns('misago.security.views',
    url(r'^signin/$', 'signin', name="sign_in"),
    url(r'^signout/$', 'signout', name="sign_out"),
)

# Include admin patterns
if ADMIN_PATH:
    urlpatterns += patterns('misago.security.views',
        url(r'^' + ADMIN_PATH + 'signout/$', 'signout', name="admin_sign_out"),
    )