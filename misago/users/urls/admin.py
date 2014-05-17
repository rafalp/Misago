from django.conf.urls import url
from misago.admin import urlpatterns
from misago.users.views.useradmin import UsersList
from misago.users.views.rankadmin import RanksList


# Users section
urlpatterns.namespace(r'^users/', 'users')


# Accounts
urlpatterns.namespace(r'^accounts/', 'accounts', 'users')
urlpatterns.patterns('users:accounts',
    url(r'^$', UsersList.as_view(), name='index'),
    url(r'^(?P<page>\d+)/$', UsersList.as_view(), name='index'),
)


# Ranks
urlpatterns.namespace(r'^ranks/', 'ranks', 'users')
urlpatterns.patterns('users:ranks',
    url(r'^$', RanksList.as_view(), name='index'),
)
