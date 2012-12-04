from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from misago.admin import AdminAction
from misago.acl.models import Role
from misago.banning.models import Ban
from misago.newsletters.models import Newsletter
from misago.users.models import User, Rank, Pruning

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
                         'name': _("Browse Users"),
                         'help': _("Browse all registered user accounts"),
                         'route': 'admin_users'
                         },
                        {
                         'id': 'new',
                         'name': _("Add User"),
                         'help': _("Create new user account"),
                         'route': 'admin_users_new'
                         },
                        ],
               route='admin_users',
               urlpatterns=patterns('misago.users.admin.users.views',
                        url(r'^$', 'List', name='admin_users'),
                        url(r'^(?P<page>\d+)/$', 'List', name='admin_users'),
                        url(r'^inactive/$', 'inactive', name='admin_users_inactive'),
                        url(r'^new/$', 'New', name='admin_users_new'),
                        url(r'^edit/(?P<slug>[a-z0-9]+)-(?P<target>\d+)/$', 'Edit', name='admin_users_edit'),
                        url(r'^delete/(?P<slug>[a-z0-9]+)-(?P<target>\d+)/$', 'Delete', name='admin_users_delete'),
                    ),
               ),
               
   AdminAction(
               section='users',
               id='roles',
               name=_("Roles"),
               help=_("Manage User Roles"),
               icon='adjust',
               model=Role,
               actions=[
                        {
                         'id': 'list',
                         'name': _("Browse Roles"),
                         'help': _("Browse all existing roles"),
                         'route': 'admin_users_roles'
                         },
                        {
                         'id': 'new',
                         'name': _("Add Role"),
                         'help': _("Create new role"),
                         'route': 'admin_users_roles_new'
                         },
                        ],
               route='admin_users_roles',
               urlpatterns=patterns('misago.users.admin.roles.views',
                        url(r'^$', 'List', name='admin_users_roles'),
                        url(r'^new/$', 'New', name='admin_users_roles_new'),
                        url(r'^edit/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Edit', name='admin_users_roles_edit'),
                        url(r'^delete/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Delete', name='admin_users_roles_delete'),
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
                         'name': _("Browse Ranks"),
                         'help': _("Browse all existing ranks"),
                         'route': 'admin_users_ranks'
                         },
                        {
                         'id': 'new',
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
                         'name': _("Browse Bans"),
                         'help': _("Browse all existing bans"),
                         'route': 'admin_users_bans'
                         },
                        {
                         'id': 'new',
                         'name': _("Set Ban"),
                         'help': _("Set new Ban"),
                         'route': 'admin_users_bans_new'
                         },
                        ],
               route='admin_users_bans',
               urlpatterns=patterns('misago.banning.admin.views',
                        url(r'^$', 'List', name='admin_users_bans'),
                        url(r'^(?P<page>\d+)/$', 'List', name='admin_users_bans'),
                        url(r'^new/$', 'New', name='admin_users_bans_new'),
                        url(r'^edit/(?P<target>\d+)/$', 'Edit', name='admin_users_bans_edit'),
                        url(r'^delete/(?P<target>\d+)/$', 'Delete', name='admin_users_bans_delete'),
                    ),
               ),
   AdminAction(
               section='users',
               id='pruning',
               name=_("Prune Users"),
               help=_("Delete multiple Users"),
               icon='remove',
               model=Pruning,
               actions=[
                        {
                         'id': 'list',
                         'name': _("Pruning Policies"),
                         'help': _("Browse all existing pruning policies"),
                         'route': 'admin_users_pruning'
                         },
                        {
                         'id': 'new',
                         'name': _("Set New Policy"),
                         'help': _("Set new pruning policy"),
                         'route': 'admin_users_pruning_new'
                         },
                        ],
               route='admin_users_pruning',
               urlpatterns=patterns('misago.users.admin.pruning.views',
                        url(r'^$', 'List', name='admin_users_pruning'),
                        url(r'^new/$', 'New', name='admin_users_pruning_new'),
                        url(r'^edit/(?P<target>\d+)/$', 'Edit', name='admin_users_pruning_edit'),
                        url(r'^delete/(?P<target>\d+)/$', 'Delete', name='admin_users_pruning_delete'),
                    ),
               ),
   AdminAction(
               section='users',
               id='newsletters',
               name=_("Newsletters"),
               help=_("Manage and send Newsletters"),
               icon='envelope',
               model=Newsletter,
               actions=[
                        {
                         'id': 'list',
                         'name': _("Browse Newsletters"),
                         'help': _("Browse all existing Newsletters"),
                         'route': 'admin_newsletters'
                         },
                        {
                         'id': 'new',
                         'name': _("New Newsletter"),
                         'help': _("Create new Newsletter"),
                         'route': 'admin_newsletters_new'
                         },
                        ],
               route='admin_newsletters',
               urlpatterns=patterns('misago.newsletters.views',
                        url(r'^$', 'List', name='admin_newsletters'),
                        url(r'^(?P<page>\d+)/$', 'List', name='admin_newsletters'),
                        url(r'^new/$', 'New', name='admin_newsletters_new'),
                        url(r'^send/(?P<target>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'send', name='admin_newsletters_send'),
                        url(r'^edit/(?P<target>\d+)/$', 'Edit', name='admin_newsletters_edit'),
                        url(r'^delete/(?P<target>\d+)/$', 'Delete', name='admin_newsletters_delete'),
                    ),
               ),
)