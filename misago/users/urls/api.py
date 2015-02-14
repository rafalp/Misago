from django.conf.urls import patterns, url


urlpatterns = patterns('misago.users.api.auth',
    url(r'^auth/$', 'authenticate', name='authenticate'),
)
