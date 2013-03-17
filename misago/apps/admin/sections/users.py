from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from misago.admin import AdminAction
from misago.models import Ban, Newsletter, PruningPolicy, Rank, User

ADMIN_ACTIONS = (
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
               urlpatterns=patterns('misago.apps.admin.users.views',
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
                         'route': 'admin_ranks'
                         },
                        {
                         'id': 'new',
                         'name': _("Add Rank"),
                         'help': _("Create new rank"),
                         'route': 'admin_ranks_new'
                         },
                        ],
               route='admin_ranks',
               urlpatterns=patterns('misago.apps.admin.ranks.views',
                        url(r'^$', 'List', name='admin_ranks'),
                        url(r'^new/$', 'New', name='admin_ranks_new'),
                        url(r'^edit/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Edit', name='admin_ranks_edit'),
                        url(r'^delete/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Delete', name='admin_ranks_delete'),
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
                         'route': 'admin_bans'
                         },
                        {
                         'id': 'new',
                         'name': _("Set Ban"),
                         'help': _("Set new Ban"),
                         'route': 'admin_bans_new'
                         },
                        ],
               route='admin_bans',
               urlpatterns=patterns('misago.apps.admin.banning.views',
                        url(r'^$', 'List', name='admin_bans'),
                        url(r'^(?P<page>\d+)/$', 'List', name='admin_bans'),
                        url(r'^new/$', 'New', name='admin_bans_new'),
                        url(r'^edit/(?P<target>\d+)/$', 'Edit', name='admin_bans_edit'),
                        url(r'^delete/(?P<target>\d+)/$', 'Delete', name='admin_bans_delete'),
                    ),
               ),
   AdminAction(
               section='users',
               id='prune_users',
               name=_("Prune Users"),
               help=_("Delete multiple Users"),
               icon='remove',
               model=PruningPolicy,
               actions=[
                        {
                         'id': 'list',
                         'name': _("Pruning Policies"),
                         'help': _("Browse all existing pruning policies"),
                         'route': 'admin_prune_users'
                         },
                        {
                         'id': 'new',
                         'name': _("Set New Policy"),
                         'help': _("Set new pruning policy"),
                         'route': 'admin_prune_users_new'
                         },
                        ],
               route='admin_prune_users',
               urlpatterns=patterns('misago.apps.admin.prune.views',
                        url(r'^$', 'List', name='admin_prune_users'),
                        url(r'^new/$', 'New', name='admin_prune_users_new'),
                        url(r'^edit/(?P<target>\d+)/$', 'Edit', name='admin_prune_users_edit'),
                        url(r'^delete/(?P<target>\d+)/$', 'Delete', name='admin_prune_users_delete'),
                        url(r'^apply/(?P<target>\d+)/$', 'Apply', name='admin_prune_users_apply'),
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
               urlpatterns=patterns('misago.apps.admin.newsletters.views',
                        url(r'^$', 'List', name='admin_newsletters'),
                        url(r'^(?P<page>\d+)/$', 'List', name='admin_newsletters'),
                        url(r'^new/$', 'New', name='admin_newsletters_new'),
                        url(r'^send/(?P<target>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'send', name='admin_newsletters_send'),
                        url(r'^edit/(?P<target>\d+)/$', 'Edit', name='admin_newsletters_edit'),
                        url(r'^delete/(?P<target>\d+)/$', 'Delete', name='admin_newsletters_delete'),
                    ),
               ),
)
