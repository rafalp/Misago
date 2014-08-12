from django.conf.urls import include, patterns, url


urlpatterns = patterns('misago.notifications.views',
    url(r'^notifications/$', 'notifications', name='notifications'),
)
