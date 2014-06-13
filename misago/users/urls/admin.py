from django.conf.urls import url
from misago.admin import urlpatterns
from misago.users.views.useradmin import UsersList, NewUser, EditUser
from misago.users.views.rankadmin import (RanksList, NewRank, EditRank,
                                          DeleteRank, MoveUpRank, MoveDownRank,
                                          DefaultRank)


# Users section
urlpatterns.namespace(r'^users/', 'users')


# Accounts
urlpatterns.namespace(r'^accounts/', 'accounts', 'users')
urlpatterns.patterns('users:accounts',
    url(r'^$', UsersList.as_view(), name='index'),
    url(r'^(?P<page>\d+)/$', UsersList.as_view(), name='index'),
    url(r'^new/$', NewUser.as_view(), name='new'),
    url(r'^edit/(?P<user_id>\d+)/$', EditUser.as_view(), name='edit'),
)


# Ranks
urlpatterns.namespace(r'^ranks/', 'ranks', 'users')
urlpatterns.patterns('users:ranks',
    url(r'^$', RanksList.as_view(), name='index'),
    url(r'^new/$', NewRank.as_view(), name='new'),
    url(r'^edit/(?P<rank_id>\d+)/$', EditRank.as_view(), name='edit'),
    url(r'^default/(?P<rank_id>\d+)/$', DefaultRank.as_view(), name='default'),
    url(r'^move/up/(?P<rank_id>\d+)/$', MoveUpRank.as_view(), name='up'),
    url(r'^move/down/(?P<rank_id>\d+)/$', MoveDownRank.as_view(), name='down'),
    url(r'^delete/(?P<rank_id>\d+)/$', DeleteRank.as_view(), name='delete'),
)
