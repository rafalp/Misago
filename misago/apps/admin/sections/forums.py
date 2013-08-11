from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from misago.admin import AdminAction
from misago.models import Forum

ADMIN_ACTIONS = (
    AdminAction(
                section='forums',
                id='forums',
                name=_("Forums List"),
                help=_("Create, edit and delete forums."),
                icon='comment',
                model=Forum,
                actions=[
                         {
                          'id': 'list',
                          'name': _("Forums List"),
                          'help': _("All existing forums"),
                          'link': 'admin_forums'
                          },
                         {
                          'id': 'new',
                          'name': _("New Node"),
                          'help': _("Create new forums tree node"),
                          'link': 'admin_forums_new'
                          },
                         ],
                link='admin_forums',
                urlpatterns=patterns('misago.apps.admin.forums.views',
                        url(r'^$', 'List', name='admin_forums'),
                        url(r'^sync/$', 'resync_forums', name='admin_forums_resync'),
                        url(r'^sync/(?P<forum>\d+)/(?P<progress>\d+)/$', 'resync_forums', name='admin_forums_resync'),
                        url(r'^new/$', 'NewNode', name='admin_forums_new'),
                        url(r'^up/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Up', name='admin_forums_up'),
                        url(r'^down/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Down', name='admin_forums_down'),
                        url(r'^edit/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Edit', name='admin_forums_edit'),
                        url(r'^delete/(?P<slug>([a-z0-9]|-)+)-(?P<target>\d+)/$', 'Delete', name='admin_forums_delete'),
                    ),
                ),
    AdminAction(
                section='forums',
                id='labels',
                name=_("Thread Labels"),
                help=_("Thread Labels allow you to group threads together within forums."),
                icon='tags',
                link='admin_forums_labels',
                urlpatterns=patterns('misago.apps.admin.index',
                        url(r'^$', 'todo', name='admin_forums_labels'),
                    ),
                ),
    AdminAction(
                section='forums',
                id='badwords',
                name=_("Words Filter"),
                help=_("Forbid usage of words in messages"),
                icon='volume-off',
                link='admin_forums_badwords',
                urlpatterns=patterns('misago.apps.admin.index',
                        url(r'^$', 'todo', name='admin_forums_badwords'),
                    ),
                ),
    AdminAction(
                section='forums',
                id='tests',
                name=_("Tests"),
                help=_("Tests that new messages have to pass"),
                icon='filter',
                link='admin_forums_tests',
                urlpatterns=patterns('misago.apps.admin.index',
                        url(r'^$', 'todo', name='admin_forums_tests'),
                    ),
                ),
    AdminAction(
                section='forums',
                id='attachments',
                name=_("Attachments"),
                help=_("Manage allowed attachment types."),
                icon='download-alt',
                link='admin_forums_attachments',
                urlpatterns=patterns('misago.apps.admin.index',
                        url(r'^$', 'todo', name='admin_forums_attachments'),
                    ),
                ),
)
