from django.conf.urls import url
from django.conf.urls import url
from django.contrib import admin as djadmin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from misago.users.views.admin.bans import BansList, NewBan, EditBan, DeleteBan
from misago.users.views.admin.ranks import (RanksList, NewRank, EditRank,
                                            DeleteRank, MoveDownRank,
                                            MoveUpRank, DefaultRank, RankUsers)
from misago.users.views.admin.users import UsersList, NewUser, EditUser
from misago.users.views.admin.warnings import (WarningsList, NewWarning,
                                               EditWarning, MoveDownWarning,
                                               MoveUpWarning, DeleteWarning)


class UserAdmin(djadmin.ModelAdmin):
    actions = None
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('groups', 'is_staff', 'is_superuser')
    readonly_fields = ('username', 'email', 'is_staff', 'is_superuser')
    fieldsets = (
        (_('User data'),
         {'fields': ('username', 'email', 'is_staff', 'is_superuser')}),
        (_('Change Django Permissions'),
         {'fields': ('groups', 'user_permissions')}),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

djadmin.site.register(get_user_model(), UserAdmin)


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
            url(r'^move/down/(?P<rank_id>\d+)/$', MoveDownRank.as_view(), name='down'),
            url(r'^move/up/(?P<rank_id>\d+)/$', MoveUpRank.as_view(), name='up'),
            url(r'^users/(?P<rank_id>\d+)/$', RankUsers.as_view(), name='users'),
            url(r'^delete/(?P<rank_id>\d+)/$', DeleteRank.as_view(), name='delete'),
        )

        # Bans
        urlpatterns.namespace(r'^bans/', 'bans', 'users')
        urlpatterns.patterns('users:bans',
            url(r'^$', BansList.as_view(), name='index'),
            url(r'^(?P<page>\d+)/$', BansList.as_view(), name='index'),
            url(r'^new/$', NewBan.as_view(), name='new'),
            url(r'^edit/(?P<ban_id>\d+)/$', EditBan.as_view(), name='edit'),
            url(r'^delete/(?P<ban_id>\d+)/$', DeleteBan.as_view(), name='delete'),
        )

        # Warnings
        urlpatterns.namespace(r'^warnings/', 'warnings', 'users')
        urlpatterns.patterns('users:warnings',
            url(r'^$', WarningsList.as_view(), name='index'),
            url(r'^new/$', NewWarning.as_view(), name='new'),
            url(r'^edit/(?P<warning_id>\d+)/$', EditWarning.as_view(), name='edit'),
            url(r'^move/down/(?P<warning_id>\d+)/$', MoveDownWarning.as_view(), name='down'),
            url(r'^move/up/(?P<warning_id>\d+)/$', MoveUpWarning.as_view(), name='up'),
            url(r'^delete/(?P<warning_id>\d+)/$', DeleteWarning.as_view(), name='delete'),
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

        site.add_node(name=_("Bans"),
                      icon='fa fa-lock',
                      parent='misago:admin:users',
                      after='misago:admin:users:ranks:index',
                      namespace='misago:admin:users:bans',
                      link='misago:admin:users:bans:index')

        site.add_node(name=_("Warning levels"),
                      icon='fa fa-exclamation-triangle',
                      parent='misago:admin:users',
                      after='misago:admin:users:bans:index',
                      namespace='misago:admin:users:warnings',
                      link='misago:admin:users:warnings:index')
