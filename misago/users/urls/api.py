from django.conf.urls import patterns, url


urlpatterns = patterns('misago.users.api.auth',
    url(r'^auth/login/$', 'login', name='login'),
    url(r'^auth/$', 'user', name='auth_user'),
)
