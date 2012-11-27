from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from misago.admin import AdminSection, AdminAction

ADMIN_SECTIONS=(
    AdminSection(
                 id='forums',
                 name=_("Forums"),
                 icon='comment',
                 after='users',
                 ),
)

ADMIN_ACTIONS=(
   AdminAction(
               section='forums',
               id='forums',
               name=_("Forums List"),
               help=_("Create, edit and delete forums."),
               icon='comment',
               route='admin_forums',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_forums'),
                    ),
               ),
   AdminAction(
               section='forums',
               id='moderators',
               name=_("Moderators"),
               help=_("Assign forums moderators."),
               icon='eye-open',
               route='admin_forums_moderators',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_forums_moderators'),
                    ),
               ),
   AdminAction(
               section='forums',
               id='tests',
               name=_("Tests"),
               help=_("Tests that new messages have to pass"),
               icon='filter',
               route='admin_forums_tests',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_forums_tests'),
                    ),
               ),
   AdminAction(
               section='forums',
               id='badwords',
               name=_("Words Filter"),
               help=_("Forbid usage of words in messages"),
               icon='volume-off',
               route='admin_forums_badwords',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_forums_badwords'),
                    ),
               ),
   AdminAction(
               section='forums',
               id='attachments',
               name=_("Attachments"),
               help=_("Manage allowed attachment types."),
               icon='download-alt',
               route='admin_forums_attachments',
               urlpatterns=patterns('misago.admin.views',
                        url(r'^$', 'todo', name='admin_forums_attachments'),
                    ),
               ),
)