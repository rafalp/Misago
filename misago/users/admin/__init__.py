from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from misago.admin import AdminSection, AdminAction
from misago.banning.models import Ban
from misago.users.models import User, Rank

ADMIN_SECTIONS=(
    AdminSection(
                 id='users',
                 name=_("Users"),
                 icon='user',
                 after='overview',
                 ),
)

ADMIN_ACTIONS=(
   AdminAction(
               section='users',
               id='users',
               name=_("Users List"),
               help=_("Search and browse users"),
               icon='user',
               model=User,
               actions=[
                        {
                         'id': 'list',
                         'icon': 'list-alt',
                         'name': _("Browse Users"),
                         'help': _("Browse all registered user accounts"),
                         'route': 'admin_users'
                         },
                        {
                         'id': 'new',
                         'icon': 'plus',
                         'name': _("Add User"),
                         'help': _("Create new user account"),
                         'route': 'admin_users_new'
                         },
                        ],
               route='admin_users',
               urlpatterns=patterns('misago.users.admin.users.views',
                        url(r'^$', 'List', name='admin_users'),
                        url(r'^inactive/$', 'inactive', name='admin_users_inactive'),
                        url(r'^new/$', 'List', name='admin_users_new'),
                        url(r'^edit/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Edit', name='admin_users_edit'),
                        url(r'^delete/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Delete', name='admin_users_delete'),
                    ),
               ),
   AdminAction(
               section='users',
               id='ranks',
               name=_("Ranks"),
               help=_("Administrate User Ranks"),
               icon='star',
               model=Rank,
               actions=[
                        {
                         'id': 'list',
                         'icon': 'list-alt',
                         'name': _("Browse Ranks"),
                         'help': _("Browse all existing ranks"),
                         'route': 'admin_users_ranks'
                         },
                        {
                         'id': 'new',
                         'icon': 'plus',
                         'name': _("Add Rank"),
                         'help': _("Create new rank"),
                         'route': 'admin_users_ranks_new'
                         },
                        ],
               route='admin_users_ranks',
               urlpatterns=patterns('misago.users.admin.ranks.views',
                        url(r'^$', 'List', name='admin_users_ranks'),
                        url(r'^new/$', 'New', name='admin_users_ranks_new'),
                        url(r'^edit/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Edit', name='admin_users_ranks_edit'),
                        url(r'^delete/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Delete', name='admin_users_ranks_delete'),
                    ),
               ),
   AdminAction(
               section='users',
               id='bans',
               name=_("Banning"),
               help=_("Ban or unban users from forums."),
               icon='lock',
               model=Ban,
               actions=[
                        {
                         'id': 'list',
                         'icon': 'list-alt',
                         'name': _("Browse Bans"),
                         'help': _("Browse all existing bans"),
                         'route': 'admin_users_bans'
                         },
                        {
                         'id': 'new',
                         'icon': 'plus',
                         'name': _("Set Ban"),
                         'help': _("Set new Ban"),
                         'route': 'admin_users_bans_new'
                         },
                        ],
               route='admin_users_bans',
               urlpatterns=patterns('misago.banning.admin.views',
                        url(r'^$', 'List', name='admin_users_bans'),
                        url(r'^new/$', 'New', name='admin_users_bans_new'),
                        url(r'^edit/(?P<target>\d+)/$', 'Edit', name='admin_users_bans_edit'),
                        url(r'^delete/(?P<target>\d+)/$', 'Delete', name='admin_users_bans_delete'),
                    ),
               ),
   AdminAction(
               section='users',
               id='prune',
               name=_("Prune Users"),
               help=_("Delete multiple Users"),
               icon='remove',
               route='admin_users_prune',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_users_prune'),
                    ),
               ),
   AdminAction(
               section='users',
               id='newsletters',
               name=_("Newsletters"),
               help=_("Manage and send Newsletters"),
               icon='envelope',
               route='admin_users_newsletters',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_users_newsletters'),
                    ),
               ),
)