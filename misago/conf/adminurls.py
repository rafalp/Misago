from django.conf.urls import url
from misago.admin import urlpatterns


urlpatterns.namespace(r'^settings/', 'settings')

urlpatterns.patterns('settings',
    url(r'^$', 'misago.conf.views.index', name='index'),
    url(r'^(?P<group_key>(\w|-)+)/$', 'misago.conf.views.group', name='group'),
)
