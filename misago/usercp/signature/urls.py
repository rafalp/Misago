from django.conf.urls import patterns, url

urlpatterns = patterns('misago.usercp.signature.views',
    url(r'^signature/$', 'signature', name="usercp_signature"),
)
