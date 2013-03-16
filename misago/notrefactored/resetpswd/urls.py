from django.conf.urls import patterns, url

urlpatterns = patterns('misago.resetpswd.views',
    url(r'^$', 'form', name="forgot_password"),
    url(r'^(?P<username>[a-z0-9]+)-(?P<user>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'reset', name="reset_password"),
)