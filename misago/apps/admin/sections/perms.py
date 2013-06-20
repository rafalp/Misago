from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from misago.admin import AdminAction
from misago.models import ForumRole, Role

ADMIN_ACTIONS = (
    AdminAction(
                section='perms',
                id='roles',
                name=_("User Roles"),
                help=_("Manage User Roles"),
                icon='th-large',
                model=Role,
                actions=[
                         {
                          'id': 'list',
                          'name': _("Browse Roles"),
                          'help': _("Browse all existing roles"),
                          'route': 'admin_roles'
                          },
                         {
                          'id': 'new',
                          'name': _("Add Role"),
                          'help': _("Create new role"),
                          'route': 'admin_roles_new'
                          },
                         ],
                route='admin_roles',
                urlpatterns=patterns('misago.apps.admin.roles.views',
                         url(r'^$', 'List', name='admin_roles'),
                         url(r'^new/$', 'New', name='admin_roles_new'),
                         url(r'^forums/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Forums', name='admin_roles_masks'),
                         url(r'^acl/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'ACL', name='admin_roles_acl'),
                         url(r'^edit/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Edit', name='admin_roles_edit'),
                         url(r'^delete/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Delete', name='admin_roles_delete'),
                     ),
                ),
    AdminAction(
                section='perms',
                id='roles_forums',
                name=_("Forum Roles"),
                help=_("Manage Forum Roles"),
                icon='th-list',
                model=ForumRole,
                actions=[
                         {
                          'id': 'list',
                          'name': _("Browse Roles"),
                          'help': _("Browse all existing roles"),
                          'route': 'admin_roles_forums'
                          },
                         {
                          'id': 'new',
                          'name': _("Add Role"),
                          'help': _("Create new role"),
                          'route': 'admin_roles_forums_new'
                          },
                         ],
                route='admin_roles_forums',
                urlpatterns=patterns('misago.apps.admin.forumroles.views',
                         url(r'^$', 'List', name='admin_roles_forums'),
                         url(r'^new/$', 'New', name='admin_roles_forums_new'),
                         url(r'^acl/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'ACL', name='admin_roles_forums_acl'),
                         url(r'^edit/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Edit', name='admin_roles_forums_edit'),
                         url(r'^delete/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Delete', name='admin_roles_forums_delete'),
                     ),
                ),
)
