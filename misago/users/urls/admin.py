from django.conf.urls import url
from misago.admin import urlpatterns
from misago.users.views.useradmin import UsersList


urlpatterns.namespace(r'^users/', 'users')
urlpatterns.namespace(r'^accounts/', 'accounts', 'users')


urlpatterns.patterns('users:accounts',
    url(r'^$', UsersList.as_view(), name='index'),
    url(r'^(?P<page>\d+)/$', UsersList.as_view(), name='index'),
)
