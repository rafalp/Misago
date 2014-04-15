from django.conf.urls import patterns, url


urlpatterns = patterns('misago.users.views.auth',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)
