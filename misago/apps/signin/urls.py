from django.conf.urls import patterns, url
from misago.admin import ADMIN_PATH

urlpatterns = patterns('misago.apps.signin.views',
    url(r'^signin/$', 'signin', name="sign_in"),
    url(r'^signout/$', 'signout', name="sign_out"),
)

# Include admin patterns
if ADMIN_PATH:
    urlpatterns += patterns('misago.apps.signin.views',
        url(r'^' + ADMIN_PATH + 'signout/$', 'signout', name="admin_sign_out"),
    )
