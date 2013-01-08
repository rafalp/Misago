from django.conf.urls import patterns, url

urlpatterns = patterns('misago.usercp.options.views',
    url(r'^$', 'options', name="usercp"),
)
