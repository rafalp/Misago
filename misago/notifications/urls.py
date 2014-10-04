from django.conf.urls import include, patterns, url


urlpatterns = patterns('misago.notifications.views',
    url(r'^notifications/$', 'notifications', name='notifications'),
    url(r'^notifications/go-to/(?P<notification_id>\d+)/(?P<trigger>[a-zA-Z0-9]+)/$', 'go_to_notification', name='go_to_notification'),
)
