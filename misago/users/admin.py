from django.conf.urls import url
from django.contrib import admin as djadmin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .djangoadmin import UserAdminModel
from .views.admin.bans import BansList, DeleteBan, EditBan, NewBan
from .views.admin.ranks import (
    DefaultRank, DeleteRank, EditRank, MoveDownRank, MoveUpRank, NewRank, RanksList, RankUsers)
from .views.admin.users import (
    DeleteAccountStep, DeletePostsStep, DeleteThreadsStep, EditUser, NewUser, UsersList)


djadmin.site.register(model_or_iterable=get_user_model(), admin_class=UserAdminModel)


class MisagoAdminExtension(object):
    def register_urlpatterns(self, urlpatterns):
        # Users section
        urlpatterns.namespace(r'^users/', 'users')

        # Accounts
        urlpatterns.namespace(r'^accounts/', 'accounts', 'users')
        urlpatterns.patterns(
            'users:accounts',
            url(r'^$', UsersList.as_view(), name='index'),
            url(r'^(?P<page>\d+)/$', UsersList.as_view(), name='index'),
            url(r'^new/$', NewUser.as_view(), name='new'),
            url(r'^edit/(?P<pk>\d+)/$', EditUser.as_view(), name='edit'),
            url(
                r'^delete-threads/(?P<pk>\d+)/$',
                DeleteThreadsStep.as_view(),
                name='delete-threads'
            ),
            url(r'^delete-posts/(?P<pk>\d+)/$', DeletePostsStep.as_view(), name='delete-posts'),
            url(
                r'^delete-account/(?P<pk>\d+)/$',
                DeleteAccountStep.as_view(),
                name='delete-account'
            ),
        )

        # Ranks
        urlpatterns.namespace(r'^ranks/', 'ranks', 'users')
        urlpatterns.patterns(
            'users:ranks',
            url(r'^$', RanksList.as_view(), name='index'),
            url(r'^new/$', NewRank.as_view(), name='new'),
            url(r'^edit/(?P<pk>\d+)/$', EditRank.as_view(), name='edit'),
            url(r'^default/(?P<pk>\d+)/$', DefaultRank.as_view(), name='default'),
            url(r'^move/down/(?P<pk>\d+)/$', MoveDownRank.as_view(), name='down'),
            url(r'^move/up/(?P<pk>\d+)/$', MoveUpRank.as_view(), name='up'),
            url(r'^users/(?P<pk>\d+)/$', RankUsers.as_view(), name='users'),
            url(r'^delete/(?P<pk>\d+)/$', DeleteRank.as_view(), name='delete'),
        )

        # Bans
        urlpatterns.namespace(r'^bans/', 'bans', 'users')
        urlpatterns.patterns(
            'users:bans',
            url(r'^$', BansList.as_view(), name='index'),
            url(r'^(?P<page>\d+)/$', BansList.as_view(), name='index'),
            url(r'^new/$', NewBan.as_view(), name='new'),
            url(r'^edit/(?P<pk>\d+)/$', EditBan.as_view(), name='edit'),
            url(r'^delete/(?P<pk>\d+)/$', DeleteBan.as_view(), name='delete'),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Users"),
            icon='fa fa-users',
            parent='misago:admin',
            after='misago:admin:index',
            namespace='misago:admin:users',
            link='misago:admin:users:accounts:index',
        )

        site.add_node(
            name=_("User Accounts"),
            icon='fa fa-users',
            parent='misago:admin:users',
            namespace='misago:admin:users:accounts',
            link='misago:admin:users:accounts:index',
        )

        site.add_node(
            name=_("Ranks"),
            icon='fa fa-graduation-cap',
            parent='misago:admin:users',
            after='misago:admin:users:accounts:index',
            namespace='misago:admin:users:ranks',
            link='misago:admin:users:ranks:index',
        )

        site.add_node(
            name=_("Bans"),
            icon='fa fa-lock',
            parent='misago:admin:users',
            after='misago:admin:users:ranks:index',
            namespace='misago:admin:users:bans',
            link='misago:admin:users:bans:index',
        )
