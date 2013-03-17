from django.conf.urls import patterns, url

urlpatterns = patterns('misago.activation.views',
    url(r'^request/$', 'form', name="send_activation"),
    url(r'^(?P<username>[a-z0-9]+)-(?P<user>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'activate', name="activate"),
)
