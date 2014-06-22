from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from misago.users.views.useradmin import UsersList, NewUser, EditUser
from misago.users.views.rankadmin import (RanksList, NewRank, EditRank,
                                          DeleteRank, MoveUpRank, MoveDownRank,
                                          DefaultRank)


class MisagoAdminExtension(object):
    def register_urlpatterns(self, urlpatterns):
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

    def register_navigation_nodes(self, site):
        site.add_node(name=_("Users"),
                      icon='fa fa-users',
                      parent='misago:admin',
                      after='misago:admin:index',
                      namespace='misago:admin:users',
                      link='misago:admin:users:accounts:index')

        site.add_node(name=_("User Accounts"),
                      icon='fa fa-users',
                      parent='misago:admin:users',
                      namespace='misago:admin:users:accounts',
                      link='misago:admin:users:accounts:index')

        site.add_node(name=_("Ranks"),
                      icon='fa fa-graduation-cap',
                      parent='misago:admin:users',
                      after='misago:admin:users:accounts:index',
                      namespace='misago:admin:users:ranks',
                      link='misago:admin:users:ranks:index')
